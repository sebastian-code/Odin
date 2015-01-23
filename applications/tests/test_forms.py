from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from applications.forms import ApplicationForm, AddApplicationSolutionForm, EMAIL_DUPLICATE_ERROR, NAMES_ERROR
from courses.models import Course
from students.models import User


class ApplicationFormTest(TestCase):

    def test_form_has_name_placeholder(self):
        form = ApplicationForm()
        self.assertIn('placeholder="Две имена"', form.as_p())

    def test_form_has_courses_choice_until_today_or_later(self):
        relevant_course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
        )
        expired_course = Course.objects.create(
            name='Expired Course',
            url='expired-course',
            application_until=datetime(1990, 1, 1),
            )
        form = ApplicationForm()
        form_courses = form.fields['course'].queryset
        self.assertIn(relevant_course, form_courses)
        self.assertNotIn(expired_course, form_courses)

    def test_form_is_not_valid_when_duplicate_email_given(self):
        course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
            )
        User.objects.create(email='foo@bar.com')
        form = ApplicationForm(data={'course': 1, 'name': 'Foo Bar', 'email': 'foo@bar.com',
                                     'skype': 'foobar', 'phone': '007'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], EMAIL_DUPLICATE_ERROR)

    def test_form_is_not_valid_when_less_than_two_names_given(self):
        course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
            )
        form = ApplicationForm(data={'course': 1, 'name': 'One', 'email': 'foo@bar.com',
        'skype': 'foobar', 'phone': '007'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], NAMES_ERROR)

    def test_form_creates_an_user_during_save(self):
        users_count_before = User.objects.count()
        users_count_after = User.objects.count()
