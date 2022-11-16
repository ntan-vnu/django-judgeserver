from django.contrib.auth.models import User
from django.db import models


class ClassProfile(models.Model):
    code = models.CharField(max_length=32)
    course = models.CharField(max_length=256)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code + '_' + self.course


class StudentProfile(models.Model):
    studentID = models.CharField(max_length=16, unique=True)
    fullName = models.CharField(max_length=64)
    classCode = models.ForeignKey(ClassProfile,
                                  related_name='students',
                                  null=True,
                                  on_delete=models.CASCADE,
                                  default=None)
    user = models.OneToOneField(User,
                                related_name='profile',
                                on_delete=models.CASCADE,
                                null=True,
                                default=None)

    def __str__(self):
        return '%s_%s_%s' % (self.classCode.code, self.studentID, self.fullName)
