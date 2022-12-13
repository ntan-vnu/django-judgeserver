from django.contrib.auth.models import User

from account.models import *
import sys

cls = 'Calculus_N01T02'
filename = '../judgeserver-test5/GiaiTichN01T02.txt'

cls = ClassProfile.objects.filter(code=cls).first()
print('import', cls)

for line in open(filename):
    studentId, lastname, firstname = line.strip().split('\t')
    fullname = lastname + ' ' + firstname
    u = User.objects.create_user(username=studentId, password=studentId)
    u.save()
    s = StudentProfile(studentID=studentId,
                       classCode=cls,
                       user=u,
                       fullName=fullname)
    s.save()
    print(s)
