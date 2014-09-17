from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from pagedown.widgets import PagedownWidget

from models import Answer


class AddPollAnswerForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.poll = kwargs.pop('poll')
        self.user = kwargs.pop('user')
        questions = self.poll.question.all()
        super(AddPollAnswerForm, self).__init__(*args, **kwargs)

        for question in questions:
            self.fields[str(question.id)] = forms.ModelChoiceField(queryset= \
            question.choice_set)

    def save(self):
        print self.cleaned_data
        print self.user