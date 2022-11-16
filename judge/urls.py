from django.urls import path

from judge import views
from judge.views import SubmissionDetailView, SubmitFormView, ExerciseDetailView

urlpatterns = [
    path('submit/', SubmitFormView.as_view(), name='submit'),
    path('submission/<int:pk>', SubmissionDetailView.as_view(), name='submission'),
    path('rejudge/<int:pk>', views.rejudge, name='rejudge'),
    path('exercise/<int:pk>', ExerciseDetailView.as_view(), name='exercise'),
]
