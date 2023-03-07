from judge.judgers import *

while True:
    s = Submission.objects.filter(state__exact=Submission.STATE_PENDING).first()
    if s:
        s.state = Submission.STATE_JUDGING
        s.save()
        if s.exercise.lang == 'java':
            j = JavaJudger(s, s.exercise)
        if s.exercise.lang == 'python':
            j = PythonJudger(s, s.exercise)
        j.judge()