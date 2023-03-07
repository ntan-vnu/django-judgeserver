from django import forms

from judge.models import Exercise, Submission


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['exercise', 'source']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exercise'].queryset = Exercise.objects.filter(
            lab__classCode__active=True, lab__active=True)
