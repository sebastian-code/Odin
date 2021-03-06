from datetime import datetime
from unittest.mock import patch

from django.core import mail
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils import timezone

from applications.forms import ApplicationForm, AddApplicationSolutionForm, ExistingUserApplicationForm, ExistingAttendingUserApplicationForm, EMAIL_DUPLICATE_ERROR, NAMES_ERROR
from applications.models import Application, ApplicationSolution, ApplicationTask
from courses.models import Course
from students.models import CourseAssignment, EducationInstitution, User


class ApplicationFormTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
        )
        self.education = EducationInstitution.objects.create(name='MIT')
        self.given_name = 'One Two'
        self.given_email = 'foo@bar.com'
        self.given_github = 'https://github.com/HackBulgaria/Odin'
        self.given_linkedin = 'https://www.linkedin.com/'
        self.form = ApplicationForm(data={'course': self.course.pk, 'name': self.given_name, 'email': self.given_email,
                                          'education': self.education.pk, 'skype': 'foobar', 'phone': '007',
                                          'linkedin_account': self.given_linkedin, 'github_account': self.given_github})

    def test_form_has_courses_choice_until_today_or_later(self):
        expired_course = Course.objects.create(
            name='Expired Course',
            url='expired-course',
            application_until=datetime(1990, 1, 1),
        )
        form_courses = self.form.fields['course'].queryset
        self.assertIn(self.course, form_courses)
        self.assertNotIn(expired_course, form_courses)

    def test_form_is_not_valid_when_duplicate_email_given(self):
        User.objects.create(email='foo@bar.com')
        form = ApplicationForm(data={'course': self.course.pk, 'name': 'Foo Bar', 'email': 'foo@bar.com',
                                     'education': self.education.pk, 'skype': 'foobar', 'phone': '007'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [EMAIL_DUPLICATE_ERROR])

    def test_form_is_not_valid_when_less_than_two_names_given(self):
        form = ApplicationForm(data={'course': self.course.pk, 'name': 'One', 'email': 'foo@bar.com',
                                     'education': self.education.pk, 'skype': 'foobar', 'phone': '007'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [NAMES_ERROR])

    def test_form_creates_an_user_during_save_without_social_accounts(self):
        users_count_before = User.objects.count()
        form = ApplicationForm(data={'course': self.course.pk, 'name': self.given_name, 'email': self.given_email,
                                     'education': self.education.pk, 'skype': 'foobar', 'phone': '007'})
        self.assertTrue(form.is_valid())
        form.save()
        users_count_after = User.objects.count()

        newly_created_user = User.objects.get(email=self.given_email)
        self.assertEqual(self.given_name, newly_created_user.get_full_name())
        self.assertEqual(self.given_email, newly_created_user.email)
        self.assertEqual(users_count_after, users_count_before + 1)

    def test_form_creates_an_user_during_save_with_social_accounts(self):
        self.assertTrue(self.form.is_valid())
        form_user = self.form.save().student
        self.assertEqual(self.given_github, form_user.github_account)
        self.assertEqual(self.given_linkedin, form_user.linkedin_account)

    @patch('django.contrib.auth.models.BaseUserManager.make_random_password')
    def test_form_emails_user(self, mocked_random_password):
        mocked_random_password.return_value = '1234'
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.form.is_valid()
            result = self.form.save()
            result_course = result.course

            subject = 'HackBulgaria application submitted for {0}'.format(result_course.name)
            context = {
                'application_until': result_course.application_until,
                'password': '1234',
                'course_name': result_course.name,
                'email': result.student.email,
                'was_registered': False,
            }
            body = render_to_string('email_application_submit.html', context)
            sent_mail = mail.outbox[0]
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(subject, sent_mail.subject)
            self.assertEqual(body, sent_mail.body)


class AddApplicationSolutionFormTest(TestCase):

    def setUp(self):
        course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
        )
        self.user = User.objects.create(email='foo@bar.com')
        self.task = ApplicationTask.objects.create(course=course,
                                                   description='task-test',
                                                   name='task for test')

    def test_saves_correctly(self):
        form = AddApplicationSolutionForm(
            data={'task': self.task.pk, 'student': self.user.pk}, user=self.user)
        application_solutions_count_before = ApplicationSolution.objects.count()
        self.assertTrue(form.is_valid())
        form.save()
        application_solutions_count_after = ApplicationSolution.objects.count()
        self.assertEqual(
            application_solutions_count_after, application_solutions_count_before + 1)


class ExistingUserApplicationFormTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
        )
        self.user = User.objects.create(email='foo@bar.com')
        self.form = ExistingUserApplicationForm(
            data={'course': self.course.pk, 'group_time': 1, 'skype': 'asd', 'phone': 54321}, user=self.user)

    def test_form_has_courses_choice_until_today_or_later(self):
        expired_course = Course.objects.create(
            name='Expired Course',
            url='expired-course',
            application_until=datetime(1990, 1, 1),
        )
        form_courses = self.form.fields['course'].queryset
        self.assertIn(self.course, form_courses)
        self.assertNotIn(expired_course, form_courses)

    def test_saves_correctly(self):
        applications_count_before = Application.objects.count()
        self.assertTrue(self.form.is_valid())
        form_result = self.form.save()
        applications_count_after = Application.objects.count()

        self.assertEqual(form_result.student, self.user)
        self.assertEqual(
            applications_count_after, applications_count_before + 1)
        self.assertEqual(Application.objects.last(), form_result)

    def test_form_emails_user(self):
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.form.is_valid()
            result = self.form.save()
            result_course = result.course

            subject = 'HackBulgaria application submitted for {0}'.format(result_course.name)
            context = {
                'application_until': result_course.application_until,
                'course_name': result_course.name,
                'email': self.user.email,
                'was_registered': True,
            }
            body = render_to_string('email_application_submit.html', context)
            sent_mail = mail.outbox[0]
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(subject, sent_mail.subject)
            self.assertEqual(body, sent_mail.body)


class ExistingAttendingUserApplicationFormTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
        )
        self.user = User.objects.create(email='foo@bar.com')
        self.form = ExistingAttendingUserApplicationForm(
            data={'course': self.course.pk, 'group_time': 1}, user=self.user)

    def test_form_has_courses_choice_until_today_or_later(self):
        expired_course = Course.objects.create(
            name='Expired Course',
            url='expired-course',
            application_until=datetime(1990, 1, 1),
        )
        form_courses = self.form.fields['course'].queryset

        self.assertIn(self.course, form_courses)
        self.assertNotIn(expired_course, form_courses)

    def test_group_time_choices(self):
        form_choices = self.form.fields['group_time'].choices
        for choice in CourseAssignment.GROUP_TIME_CHOICES:
            self.assertIn(choice, form_choices)

    def test_saves_correctly(self):
        assigments_count_before = CourseAssignment.objects.count()
        self.assertTrue(self.form.is_valid())
        form_result = self.form.save()
        assigments_count_after = CourseAssignment.objects.count()

        self.assertEqual(assigments_count_after, assigments_count_before + 1)
        self.assertEqual(CourseAssignment.objects.last(), form_result)
        self.assertEqual(CourseAssignment.objects.last().user, self.user)

    def test_form_emails_user(self):
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.form.is_valid()
            result = self.form.save()
            result_course = result.course

            subject = 'HackBulgaria application submitted for {0}'.format(result_course.name)
            context = {
                'application_until': result_course.application_until,
                'course_name': result_course.name,
                'email': self.user.email,
                'was_registered': True,
            }
            body = render_to_string('email_application_submit.html', context)
            sent_mail = mail.outbox[0]
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(subject, sent_mail.subject)
            self.assertEqual(body, sent_mail.body)
