from django.db import models
from django.db.models import Avg, Sum
from django.utils import timezone

from account.models import ClassProfile, StudentProfile


class Laboratory(models.Model):
    code = models.CharField(max_length=32)
    shortName = models.CharField(max_length=64, null=True)
    classCode = models.ManyToManyField(ClassProfile,
                                       related_name='labs')

    def __str__(self):
        return self.shortName


class Exercise(models.Model):
    code = models.CharField(max_length=16)
    lang = models.CharField(max_length=16, default='')
    description = models.TextField(max_length=4096, default='', blank=True)
    supportScript = models.TextField(max_length=65536, blank=True, default='')
    judgeScript = models.TextField(max_length=65536, blank=True, default='')
    testcaseIn = models.TextField(max_length=4096, blank=True, default='')
    testcaseOut = models.TextField(max_length=4096, blank=True, default='')
    lab = models.ForeignKey(Laboratory,
                            related_name='exercises',
                            null=True,
                            on_delete=models.CASCADE)

    def __str__(self):
        return self.lab.code + '_' + self.code


class Submission(models.Model):
    student = models.ForeignKey(StudentProfile,
                                related_name='submissions',
                                on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise,
                                 related_name='submissions',
                                 on_delete=models.CASCADE)
    state = models.CharField(max_length=32,
                             choices=[('pending', 'pending'), ('error', 'error'), ('accepted', 'accepted')],
                             default='pending')
    log = models.TextField(max_length=4096, default='', blank=True)
    score = models.FloatField(default=0)
    sDatetime = models.DateTimeField(null=True, default=timezone.now)
    source = models.TextField(max_length=65536, blank=True, default='')

    def __str__(self):
        return str(self.exercise) + '_' + self.student.studentID


class Result(models.Model):
    lab = models.ForeignKey(Laboratory, related_name='+',
                            on_delete=models.CASCADE,
                            null=True)
    score = models.FloatField(default=0)
    student = models.ForeignKey(StudentProfile, related_name='results',
                                on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, related_name='+',
                                 on_delete=models.CASCADE,
                                 null=True)

    @staticmethod
    def updateResult(std: StudentProfile, lab: Laboratory,
                     ex: Exercise, sms: Submission) -> None:
        result = Result.objects.filter(lab=lab, student=std, exercise=ex).first()
        if result is None:
            result = Result(lab=lab, student=std, exercise=ex)
        if sms.score > result.score:
            result.score = sms.score
        result.save()

    @staticmethod
    def getResultsByStudent(currentClass: ClassProfile,
                            std: StudentProfile) -> list:
        labs = currentClass.labs.all()
        results = [None] * labs.count()
        for i in range(len(results)):
            r = Result.objects.filter(lab=labs[i], student=std) \
                .aggregate(Sum('score'))['score__sum']
            r = r if r is not None else 0.
            num = labs[i].exercises.count()
            if num == 0:
                results[i] = 0
            else:
                results[i] = r / num
        return results

    @staticmethod
    def getResultsByClass(cls: ClassProfile) -> list:
        results = []
        for std in cls.students.all():
            row = [std.studentID, std.fullName]
            tmp = Result.getResultsByStudent(cls, std)
            row += tmp
            if len(tmp) > 0:
                row.append(sum(tmp) / len(tmp))
            else:
                row.append('-')
            results.append(row)
        return results
