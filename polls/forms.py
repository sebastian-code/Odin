from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from pagedown.widgets import PagedownWidget

from models import Answer


class AddPollAnswerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddPollAnswerForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super(AddPollAnswerForm, self).save(commit=False)
        instance.user = self.user
        instance.save()
        return instance

    class Meta:
        model = Answer

        fields = (
            'choice',
            'user',
        )
