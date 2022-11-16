from django.contrib import admin

from judge.models import Laboratory, Exercise, Submission, Result

admin.site.register(Laboratory)
admin.site.register(Exercise)
admin.site.register(Submission)
admin.site.register(Result)