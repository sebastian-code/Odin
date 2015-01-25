from django import forms
from django.template.loader import render_to_string
from django.utils import timezone

from applications.models import Application, ApplicationSolution
from students.models import User
from courses.models import Course
from students.validators import validate_github, validate_linkedin


EMAIL_DUPLICATE_ERROR = 'Този email вече е регистриран.'
NAMES_ERROR = 'Моля въведете поне две имена.'


class ApplicationForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        label='За кой курс кандидатстваш',
        queryset=Course.objects.filter(application_until__gte=timezone.now())
    )
    name = forms.CharField(label='Как се казваш', widget=forms.TextInput(attrs={'placeholder': 'Две имена'}), max_length=100)
    email = forms.EmailField(label='Email')
    skype = forms.CharField(label='Skype', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=100)
    github_account = forms.CharField(label='Github', widget=forms.TextInput(attrs={'placeholder': 'https://github.com/HackBulgaria'}), max_length=100, validators=[validate_github])
    linkedin_acount = forms.CharField(label='Linkedin', widget=forms.TextInput(attrs={'placeholder': 'https://www.linkedin.com/'}), max_length=100, validators=[validate_linkedin])

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid

        if User.is_existing(self.cleaned_data['email']):
            self.add_error('email', EMAIL_DUPLICATE_ERROR)
            return False

        if len(self.cleaned_data['name'].split(' ')) < 2:
            self.add_error('name', NAMES_ERROR)
            return False
        return True

    def save(self):
        course = self.cleaned_data['course']
        course_name = course.name
        email = self.cleaned_data['email']
        github_account = self.cleaned_data['github_account']
        linkedin_account = self.cleaned_data['linkedin_account']
        name = self.cleaned_data['name']
        password = User.objects.make_random_password()

        new_user = User.objects.create_user(email=email, password=password,
                                            github_account=github_account,
                                            linkedin_account=linkedin_account)
        new_user.set_full_name(name)
        new_user.save()

        self.instance.student = new_user

        context = {
            'course_name': course_name,
            'email': new_user.email,
            'password': password,
        }
        message = render_to_string('email_application_submit.html', context)
        subject = 'HackBulgaria application submitted for {0}'.format(course_name)
        self.instance.email_student(subject, message)
        return super().save()

    class Meta:
        model = Application
        fields = (
            'course',
        )


class AddApplicationSolutionForm(forms.ModelForm):

    class Meta:
        model = ApplicationSolution

        fields = (
            'task',
            'student',
        )
