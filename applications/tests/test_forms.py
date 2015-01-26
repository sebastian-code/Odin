from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from applications.forms import ApplicationForm, AddApplicationSolutionForm, ExistingUserApplicationForm, EMAIL_DUPLICATE_ERROR, NAMES_ERROR
from applications.models import ApplicationSolution, ApplicationTask
from courses.models import Course
from students.models import CourseAssignment, User


class ApplicationFormTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
        )

    def test_form_has_name_placeholder(self):
        form = ApplicationForm()
        self.assertIn('placeholder="Две имена"', form.as_p())

    def test_form_has_courses_choice_until_today_or_later(self):
        expired_course = Course.objects.create(
            name='Expired Course',
            url='expired-course',
            application_until=datetime(1990, 1, 1),
        )
        form = ApplicationForm()
        form_courses = form.fields['course'].queryset
        self.assertIn(self.course, form_courses)
        self.assertNotIn(expired_course, form_courses)

    def test_form_is_not_valid_when_duplicate_email_given(self):
        User.objects.create(email='foo@bar.com')
        form = ApplicationForm(data={'course': self.course.pk, 'name': 'Foo Bar', 'email': 'foo@bar.com',
                                     'skype': 'foobar', 'phone': '007'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [EMAIL_DUPLICATE_ERROR])

    def test_form_is_not_valid_when_less_than_two_names_given(self):
        form = ApplicationForm(data={'course': self.course.pk, 'name': 'One', 'email': 'foo@bar.com',
                                     'skype': 'foobar', 'phone': '007'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [NAMES_ERROR])

    def test_form_creates_an_user_during_save(self):
        users_count_before = User.objects.count()
        given_name = 'One Two'
        given_email = 'foo@bar.com'
        form = ApplicationForm(data={'course': self.course.pk, 'name': given_name, 'email': given_email,
                                     'skype': 'foobar', 'phone': '007'})
        self.assertTrue(form.is_valid())
        form.save()
        users_count_after = User.objects.count()

        newly_created_user = User.objects.get(email=given_email)
        self.assertEqual(given_name, newly_created_user.get_full_name())
        self.assertEqual(given_email, newly_created_user.email)
        self.assertEqual(users_count_after, users_count_before + 1)


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
        form = AddApplicationSolutionForm(data={'task': self.task.pk, 'student': self.user.pk})
        application_solutions_count_before = ApplicationSolution.objects.count()
        self.assertTrue(form.is_valid())
        form.save()
        application_solutions_count_after = ApplicationSolution.objects.count()
        self.assertEqual(application_solutions_count_after, application_solutions_count_before + 1)


class ExistingUserApplicationFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='foo@bar.com')
        self.form = ExistingUserApplicationForm(data={'group_time': 1}, user=self.user)

    def test_group_time_choices(self):
        form_choices = self.form.fields['group_time'].queryset
        self.assertEqual(CourseAssignment.GROUP_TIME_CHOICES, form_choices)

    def test_saves_correctly(self):
        assigments_count_before = CourseAssignment.objects.count()
        self.assertTrue(self.form.is_valid())
        self.form.save()
        assigments_count_after = CourseAssignment.objects.count()
        self.assertEqual(assigments_count_after, assigments_count_before + 1)
        self.assertIs(CourseAssignment.objects.last(), self.form.instance)
