from django.contrib import admin

from account.models import *


class ClassProfileAdmin(admin.ModelAdmin):
    list_display = ['code', 'course', 'active']


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['studentID', 'fullName', 'classCode']


admin.site.register(ClassProfile, ClassProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
