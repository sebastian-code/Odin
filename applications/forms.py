from django import forms
from django.utils import timezone

from applications.models import Application, ApplicationSolution
from students.models import User
from courses.models import Course


EMAIL_DUPLICATE_ERROR = 'Този email вече е регистриран.'
NAMES_ERROR = 'Моля въведете поне две имена.'


class ApplicationForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        label='За кой курс кандидатстваш',
        queryset=Course.objects.filter(application_until__gt=timezone.now())
    )
    name = forms.CharField(label='Как се казваш', widget=forms.TextInput(attrs={'placeholder': 'Две имена'}), max_length=100)
    email = forms.EmailField(label='Email')
    skype = forms.CharField(label='Skype', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=100)

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid

        if User.is_existing(self.cleaned_data['email']):
            self._errors['email_registered'] = EMAIL_DUPLICATE_ERROR
            return False

        if len(self.cleaned_data['name'].split()) < 2:
            self._errors['name_not_full'] = NAMES_ERROR
            return False
        return True

    def save(self):
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        password = User.generate_password()

        new_user = User.objects.create_user(email, password)
        new_user.set_full_name(name)
        new_user.save()

        self.instance.student = new_user
        return super().save()

    class Meta:
        model = Application
        fields = (
            'course',
        )


class AddApplicationSolutionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.student = self.user
        return super().save()

    class Meta:
        model = ApplicationSolution

        fields = (
            'task',
            'student',
        )
