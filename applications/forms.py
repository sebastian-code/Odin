from django import forms
from django.template.loader import render_to_string
from django.utils import timezone

from applications.models import Application, ApplicationSolution
from courses.models import Course
from students.models import CourseAssignment
from students.models import EducationInstitution, User


EMAIL_DUPLICATE_ERROR = 'Този email вече е регистриран.'
NAMES_ERROR = 'Моля въведете две имена.'


class ApplicationForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        label='За кой курс кандидатстваш',
        queryset=Course.objects.filter(application_until__gte=timezone.now())
    )
    name = forms.CharField(label='Как се казваш', widget=forms.TextInput(attrs={'placeholder': 'Две имена'}), max_length=100)
    education = forms.ModelChoiceField(
        label='Къде учиш',
        queryset=EducationInstitution.objects.all())
    email = forms.EmailField(label='Email')
    skype = forms.CharField(label='Skype', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=100)
    github_account = forms.CharField(label='Github', widget=forms.TextInput(attrs={'placeholder': 'https://github.com/HackBulgaria'}), max_length=100, required=False)
    linkedin_account = forms.CharField(label='Linkedin', widget=forms.TextInput(attrs={'placeholder': 'https://www.linkedin.com/'}), max_length=100, required=False)

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
        new_user.save()
        self.instance.student = new_user

        course = self.cleaned_data['course']
        context = {
            'application_until': course.application_until,
            'course_name': course.name,
            'email': email,
            'not_registered': True,
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
        label='За кой курс кандидатстваш',
        queryset=Course.objects.filter(application_until__gte=timezone.now())
    )
    skype = forms.CharField(label='Skype', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=100)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ExistingUserApplicationForm, self).__init__(*args, **kwargs)

    def save(self):
        course = self.cleaned_data['course']

        context = {
            'application_until': course.application_until,
            'course_name': course.name,
            'email': self.user.email,
            'not_registered': False,
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
        queryset=Course.objects.filter(application_until__gte=timezone.now())
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
            'not_registered': False,
        }
        message = render_to_string('email_application_submit.html', context)
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
        )
