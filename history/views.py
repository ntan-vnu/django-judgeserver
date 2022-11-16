from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from account.models import ClassProfile
from judge.models import Submission, Result


def history(request: HttpRequest) -> HttpResponse:
    if request.user.is_superuser:
        currentClass = ClassProfile.objects.get(active=True)
        smss = Submission.objects \
            .filter(exercise__lab__classCode=currentClass).all() \
            .order_by('-sDatetime')
        context = {
            'cls': currentClass,
            'labs': currentClass.labs.all(),
            'results': Result.getResultsByClass(currentClass),
            'submissions': smss
        }
        return render(request, 'history.html', context=context)
    else:
        return HttpResponse('Admin only.')

