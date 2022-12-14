from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from account.models import ClassProfile
from judge.models import Submission, Result


def history(request: HttpRequest) -> HttpResponse:
    if request.user.is_superuser:
        currentClass = ClassProfile.objects.get(active=True)
        submissions = Submission.objects \
            .filter(student__classCode=currentClass).all() \
            .order_by('-sDatetime')
        context = {
            'cls': currentClass,
            'labs': currentClass.labs.all(),
            'results': Result.getResultsByClass(currentClass),
            'submissions': submissions
        }
        return render(request, 'history/history.html', context=context)
    else:
        return HttpResponse('Admin only.')

