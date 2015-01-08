from django import forms
from django.utils import timezone

from students.models import User
from courses.models import Course


class ApplicationForm(forms.Form):
    course = forms.ModelChoiceField(
        label='За кой курс кандидатстваш',
        queryset=Course.objects.filter(application_until__gt=timezone.now())
    )
    name = forms.CharField(label='Как се казваш', max_length=100)
    email = forms.EmailField(label='Email')
    skype = forms.CharField(label='Skype', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=100)

    def is_valid(self):
        valid = super(ApplicationForm, self).is_valid()

        if not valid:
            return valid

        if User.is_existing(self.cleaned_data['email']):
            self._errors['email_registered'] = 'Този email вече е регистриран.'
            return False

        if len(self.cleaned_data['name'].split()) != 2:
            self._errors['name_not_full'] = 'Моля въведете поне две имена.'
            return False

        return True
