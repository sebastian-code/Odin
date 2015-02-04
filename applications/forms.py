from django import forms
from django.template.loader import render_to_string
from django.utils import timezone

from applications.models import Application, ApplicationSolution
from courses.models import Course
from students.models import CourseAssignment
from students.models import EducationInstitution, User


EMAIL_DUPLICATE_ERROR = 'Ти вече имаш акаунт в нашата система! Влез в него и кандидатсвай оттам.'
NAMES_ERROR = 'Моля въведи две имена.'


class ApplicationForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        label='За кой курс кандидатстваш* ',
        queryset=Course.objects.filter(application_until__gte=timezone.now()),
        initial=0
    )
    name = forms.CharField(
        label='Как се казваш (две имена)* ',
        max_length=100
    )
    email = forms.EmailField(label='Email* ')
    skype = forms.CharField(label='Skype* ', max_length=100)
    phone = forms.CharField(label='Телефон* ', max_length=100)
    education = forms.CharField(
        label='Къде учиш',
        max_length=110,
        required=False
    )
    works_at = forms.CharField(
        label='Къде работиш',
        max_length=110,
        required=False
    )
    github_account = forms.CharField(
        label='Github',
        widget=forms.TextInput(attrs={'placeholder': 'https://github.com/HackBulgaria'}),
        max_length=100,
        required=False
    )
    linkedin_account = forms.CharField(
        label='Linkedin',
        widget=forms.TextInput(attrs={'placeholder': 'https://www.linkedin.com/'}),
        max_length=100,
        required=False
    )

    def clean(self):
        cleaned_data = super(ApplicationForm, self).clean()
        email = cleaned_data.get('email')
        name = cleaned_data.get('name', '')

        if User.is_existing(email):
            self.add_error('email', EMAIL_DUPLICATE_ERROR)
        if len(name.split(' ')) < 2:
            self.add_error('name', NAMES_ERROR)

        return cleaned_data

    def save(self):
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        password = User.objects.make_random_password()

        new_user = User.objects.create_user(email=email, password=password)
        new_user.set_full_name(name)
        new_user.linkedin_account = self.cleaned_data.get('linkedin_account', '')
        new_user.github_account = self.cleaned_data.get('github_account', '')
        new_user.studies_at = self.cleaned_data.get('education', '')
        new_user.works_at = self.cleaned_data.get('works_at', '')

        new_user.save()
        self.instance.student = new_user

        course = self.cleaned_data['course']
        context = {
            'application_until': course.application_until,
            'course_name': course.name,
            'email': email,
            'was_registered': False,
            'password': password,
        }
        message = render_to_string('email_application_submit.html', context)
        subject = 'HackBulgaria application submitted for {0}'.format(course.name)
        self.instance.email_student(subject, message)
        return super().save()

    class Meta:
        model = Application
        fields = (
            'course',
        )


class ExistingUserApplicationForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        label='За кой курс кандидатстваш* ',
        queryset=Course.objects.filter(application_until__gte=timezone.now()),
        initial=0
    )
    skype = forms.CharField(label='Skype* ', max_length=100)
    phone = forms.CharField(label='Телефон* ', max_length=100)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ExistingUserApplicationForm, self).__init__(*args, **kwargs)

    def save(self):
        course = self.cleaned_data['course']

        context = {
            'application_until': course.application_until,
            'course_name': course.name,
            'email': self.user.email,
            'was_registered': True,
        }
        message = render_to_string('email_application_submit.html', context)
        subject = 'HackBulgaria application submitted for {0}'.format(course.name)
        self.instance.student = self.user
        self.user.send_email(subject, message)
        return super().save()

    class Meta:
        model = Application
        fields = (
            'course',
        )


class ExistingAttendingUserApplicationForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        label='За кой курс кандидатстваш',
        queryset=Course.objects.filter(application_until__gte=timezone.now()),
        initial=0
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ExistingAttendingUserApplicationForm, self).__init__(*args, **kwargs)

    def save(self):
        course = self.cleaned_data['course']

        context = {
            'application_until': course.application_until,
            'course_name': course.name,
            'email': self.user.email,
            'was_registered': True,
            'course_repo': course.git_repository,
        }

        message = render_to_string('email_attending_user.html', context)
        subject = 'HackBulgaria application submitted for {0}'.format(course.name)
        self.instance.user = self.user
        self.user.send_email(subject, message)
        return super().save()

    class Meta:
        model = CourseAssignment
        fields = (
            'course',
            'group_time',
        )


class AddApplicationSolutionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddApplicationSolutionForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.student = self.user
        return super(AddApplicationSolutionForm, self).save()

    class Meta:
        model = ApplicationSolution

        fields = (
            'task',
            'repo'
        )
