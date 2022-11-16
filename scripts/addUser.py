from django.contrib.auth.models import User

from account.models import *
import sys

cls = 'N07T01'
filename = '../judgeserver-test2/DSA_N07T01.txt'

cls = ClassProfile.objects.filter(code=cls).first()
print('import', cls)

for line in open(filename):
    studentId, fullname = line.strip().split('\t')
    u = User.objects.create_user(username=studentId, password=studentId)
    u.save()
    s = StudentProfile(studentID=studentId,
                       classCode=cls,
                       user=u,
                       fullName=fullname)
    s.save()
    print(s)
