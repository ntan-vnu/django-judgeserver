from django import forms

from judge.models import Submission


class SubmitForm(forms.ModelForm):

    class Meta:
        model = Submission
        fields = ['exercise', 'source']

