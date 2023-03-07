from django.contrib.auth.models import User

from account.models import *
import sys

cls = 'OOP-N06T01'
filename = 'OOP-N06T01.txt'

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
