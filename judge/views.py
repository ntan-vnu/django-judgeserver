from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, FormView

from account.models import ClassProfile
from judge.forms import SubmitForm
from judge.models import Submission, Result, Exercise


@login_required
def home(request: HttpRequest) -> HttpResponse:
    user = request.user
    if user.is_superuser:
        return redirect('/history')
    currentClass = get_object_or_404(ClassProfile, active=True)
    # currentClass = ClassProfile.objects.filter(active=True).first()
    labs = currentClass.labs.all()
    results = Result.getResultsByStudent(currentClass, user.profile)
    submissions = Submission.objects \
        .filter(student=user.profile) \
        .all().order_by('-sDatetime')
    context = {'site_header': str(currentClass),
               'submissions': submissions,
               'labs': labs,
               'user': user,
               'results': results}
    return render(request, template_name='home.html',
                  context=context)


class SubmitFormView(LoginRequiredMixin, FormView):
    login_url = 'account:login'
    template_name = 'judge/submit.html'
    form_class = SubmitForm
    success_url = '/'

    def form_valid(self, form):
        submission = form.save(commit=False)
        submission.student = self.request.user.profile
        submission.save()
        return super().form_valid(form)


class SubmissionDetailView(LoginRequiredMixin, DetailView):
    login_url = 'account:login'
    model = Submission
    template_name = 'judge/submission.html'


class ExerciseDetailView(LoginRequiredMixin, DetailView):
    login_url = 'account:login'
    model = Exercise
    template_name = 'judge/exercise.html'


@login_required
def rejudge(request: HttpRequest, pk) -> HttpResponse:
    if request.user.is_superuser:
        sms = Submission.objects.get(pk=pk)
        sms.state = 'pending'
        sms.save()
        return redirect('/history')
    else:
        return HttpResponse('Admin only.')
