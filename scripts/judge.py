from judge.models import *
from judge.judgers import *

while True:
    s = Submission.objects.filter(state__exact='pending').first()
    if s:
        if s.exercise.lang == 'java':
            j = JavaJudger(s, s.exercise)
        if s.exercise.lang == 'python':
            j = PythonJudger(s, s.exercise)
        j.judge()
