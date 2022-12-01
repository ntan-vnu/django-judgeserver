import datetime
import os
import secrets
import subprocess

from judge.models import Submission, Exercise, Result


class BaseJudger:
    JUDGING_DIR = 'judgings/'

    def __init__(self, sms: Submission, ex: Exercise):
        self.workingDir = None
        self.sms = sms
        self.ex = ex
        self.numTestcase = 0
        self.cmdSep = '&' if os.name == 'nt' else ';'

    def createWorkingDir(self) -> str:
        self.workingDir = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        self.workingDir += '-' + self.sms.student.studentID + '-' + secrets.token_hex(8)
        self.workingDir = os.path.join(self.JUDGING_DIR, self.workingDir)
        if not os.path.exists(self.workingDir):
            os.mkdir(self.workingDir)
        return self.workingDir

    def writeScript(self) -> None:
        pass

    def compile(self) -> None:
        pass

    def evaluate(self) -> float:
        return 0

    def compare(self, i):
        fout = open(self.workingDir + '/%03d.out' % i).read()
        fans = open(self.workingDir + '/%03d.ans' % i).read()
        outTerms = fout.split()
        ansTerms = fans.split()
        for i in range(len(outTerms)):
            print(outTerms[i], ansTerms[i])
            if outTerms[i] != ansTerms[i]:
                return 0
        return 1

    def extractTestcases(self, ex: Exercise):
        count = 0
        testcaseIth = []
        for line in ex.testcaseIn.split('\n'):
            if line.strip() == '@':
                with open(self.workingDir + '/%03d.in' % count, 'wt') as g:
                    g.writelines(testcaseIth)
                testcaseIth = []
                count += 1
            else:
                testcaseIth.append(line)

        count = 0
        testcaseIth = []
        for line in ex.testcaseOut.split('\n'):
            if line.strip() == '@':
                with open(self.workingDir + '/%03d.ans' % count, 'wt') as g:
                    g.writelines(testcaseIth)
                testcaseIth = []
                count += 1
            else:
                testcaseIth.append(line)
        self.numTestcase = count

    def judge(self) -> float:
        try:
            self.sms.log = ''
            print('#judging.', 'created.', self.createWorkingDir())
            self.extractTestcases(self.ex)
            print('#judging.', 'extracted testcases.', self.numTestcase)
            self.writeScript()
            print('#judging.', 'wrote script.')
            try:
                self.compile()
            except Exception as e:
                self.sms.log += str(e)
                self.sms.state = 'error'
                self.sms.save()
                print('#judging.', 'compile error.', e)
                return 0
            print('#judging.', 'compiled.')

            self.sms.score = self.evaluate()
            print('#judging.', 'evaluated.')
            self.sms.state = 'accepted'
            self.sms.save()
            print('#judging.', 'finished.', self.sms.score, '/ 10.0')

            Result.updateResult(self.sms.student,
                                self.sms.exercise.lab,
                                self.sms.exercise,
                                self.sms)
        except Exception as e:
            self.sms.log += str(e)
            self.sms.state = 'error'
            self.sms.save()
            print(e)

    def runProcess(self, cmd, timeout=3):
        subprocess.run(cmd, timeout=timeout, shell=True)


class JavaJudger(BaseJudger):
    def writeScript(self) -> None:
        script = self.ex.supportScript + \
                 '\n\n\n' + self.sms.source + \
                 '\n\n\n' + self.ex.judgeScript
        with open(self.workingDir + '/Main.java', 'wt') as g:
            g.write(script)

    def compile(self) -> None:
        code = os.system('cd {0}{1} javac Main.java > compile.log 2>&1'
                         .format(self.workingDir, self.cmdSep))
        log_msg = open(self.workingDir + '/compile.log').read()
        assert code == 0, Exception(log_msg)

    def evaluate(self) -> float:
        score = 0
        for i in range(self.numTestcase):
            try:
                cmd = 'cd {0} {1} java Main < {2:03d}.in > {2:03d}.out' \
                    .format(self.workingDir, self.cmdSep, i)
                print(cmd)
                self.runProcess(cmd)
                s = self.compare(i)
                print('#judging.', 'scored testcase.%03d.' % i, s)
                score += s
            except Exception as e:
                self.sms.log += '#evaluating\n' + str(e)
                print(e)
        return score * 10. / self.numTestcase


class PythonJudger(BaseJudger):
    def writeScript(self) -> None:
        script = self.ex.supportScript + \
                 '\n\n\n' + self.sms.source + \
                 '\n\n\n' + self.ex.judgeScript
        with open(self.workingDir + '/main.py', 'wt') as g:
            g.write(script)

    def evaluate(self) -> float:
        score = 0
        for i in range(self.numTestcase):
            try:
                code = os.system('cd {0} {1} python main.py < {2:03d}.in > {2:03d}.out'
                                 .format(self.workingDir, self.cmdSep, i))
                assert code == 0, Exception('run error. testcase{0}'.format(i))
                s = self.compare(i)
                print('#judging.', 'scored testcase.%03d.' % i, s)
                score += s
            except Exception as e:
                self.sms.log += 'evaluating\n' + str(e)
                self.sms.save()
                print(e)
        return score * 10. / self.numTestcase
