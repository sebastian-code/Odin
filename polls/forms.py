from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from models import Choice, Answer


class AddPollAnswerForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.poll = kwargs.pop('poll')
        self.user = kwargs.pop('user')
        self.questions = self.poll.question.all()
        super(AddPollAnswerForm, self).__init__(*args, **kwargs)

        for question in self.questions:
            self.fields[str(question.id)] = forms.ModelChoiceField(queryset=question.choice_set)
            self.fields[str(question.id)].label = question.title

    def save(self):
        for choice in self.cleaned_data.values():
            Answer.objects.create(choice=choice, user=self.user)
