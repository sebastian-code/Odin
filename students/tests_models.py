import datetime
import mock

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase


from .models import CheckIn, User, HrLoginLog, CourseAssignment, Solution, StudentStartedWorkingAt
from courses.models import Partner, Course, Task


class UserManagerModelTest(TestCase):

    def setUp(self):
        self.email = 'user@internet.com'
        self.raw_password = 'abc123'

    def test_create_user(self):
        result = User.objects.create_user(self.email, self.raw_password)
        hashed_password = make_password(self.raw_password)
        self.assertRaises(IntegrityError, User.objects.create, username=self.email, password=hashed_password)
        self.assertEqual(self.email, result.username)

    def test_create_user_with_invalid_email(self):
        self.assertRaises(ValueError, User.objects.create_user, email=None, password=self.raw_password)

    def test_create_superuser(self):
        result = User.objects.create_superuser(self.email, self.raw_password)
        self.assertTrue(result.is_superuser)
        self.assertTrue(result.is_staff)


class UserModelTest(TestCase):

    def setUp(self):
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.mac = '4c:80:93:1f:a4:50'
        self.student_user.save()

        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
        )
        self.course2 = Course.objects.create(
            name='Test Course2',
            url='test-course2',
            application_until=datetime.datetime.now(),
        )
        self.assignment = CourseAssignment.objects.create(
            user=self.student_user, course=self.course, group_time=CourseAssignment.EARLY)

    def test_unicode(self):
        self.assertEqual(self.student_user.get_full_name(), unicode(self.student_user))

    def test_get_avatar_url(self):
        self.student_user.avatar = None
        self.assertEqual(settings.STATIC_URL + settings.NO_AVATAR_IMG, self.student_user.get_avatar_url())
        self.student_user.avatar = 'Kappa.jpg'
        self.assertEqual('/media/Kappa.jpg', self.student_user.get_avatar_url())

    def test_get_courses(self):
        self.assertEqual(u'Test Course - 1', self.student_user.get_courses())
        CourseAssignment.objects.create(
            user=self.student_user, course=self.course2, group_time=CourseAssignment.LATE)
        self.assertEqual(u'Test Course - 1; Test Course2 - 2', self.student_user.get_courses())

    def test_get_courses_list(self):
        self.assertEqual([self.assignment], self.student_user.get_courses_list())
        assignment2 = CourseAssignment.objects.create(
            user=self.student_user, course=self.course2, group_time=CourseAssignment.LATE)
        self.assertEqual([self.assignment, assignment2], self.student_user.get_courses_list())

    def test_is_existing(self):
        self.assertFalse(User.is_existing('referee@real-madrid.com'))
        self.assertTrue(User.is_existing('ivo_student@gmail.com'))

    @mock.patch('students.models.random')
    def test_generate_password(self, mocked_random):
        mocked_random.choice = mock.Mock(return_value='1')
        expected = '111111111'
        self.assertEqual(expected, User.generate_password())


class CourseAssignmentModelTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
            end_time=datetime.date.today(),
            ask_for_feedback=True
        )

        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.first_name = 'Ivaylo'
        self.student_user.last_name = 'Bachvarov'
        self.student_user.status = User.STUDENT
        self.student_user.save()

        self.partner_potato = Partner.objects.create(
            name='Potato Company', description='Potato company')
        self.partner_salad = Partner.objects.create(
            name='Salad Company', description='Salad Company')

        self.hr_user = User.objects.create_user('ivan_hr@gmail.com', '1234')
        self.hr_user.status = User.HR
        self.hr_user.hr_of = self.partner_potato
        self.hr_user.save()

        self.assignment = CourseAssignment.objects.create(
            user=self.student_user, course=self.course, group_time=CourseAssignment.EARLY)
        self.assignment.favourite_partners.add(self.partner_potato)
        self.third_wheel = User.objects.create_user('third_wheel@gmail.com', '456')

    def test_unicode(self):
        self.assertEqual('<Ivaylo Bachvarov> Test Course - 1', unicode(self.assignment))

    def test_get_favourite_partners(self):
        self.assertEqual('Potato Company', self.assignment.get_favourite_partners())
        self.assignment.favourite_partners.add(self.partner_salad)
        self.assertEqual('Potato Company; Salad Company', self.assignment.get_favourite_partners())

    def test_has_valid_github_account(self):
        self.assertFalse(self.assignment.has_valid_github_account())
        self.student_user.github_account = 'http://hackbulgaria.com'
        self.assertFalse(self.assignment.has_valid_github_account())

        self.student_user.github_account = 'https://github.com/Ivaylo-Bachvarov'
        self.assertTrue(self.assignment.has_valid_github_account())


class StudentStartedWorkingAtModelTest(TestCase):

    def setUp(self):
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.first_name = 'Ivaylo'
        self.student_user.last_name = 'Bachvarov'
        self.student_user.status = User.STUDENT
        self.student_user.save()

        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
        )
        self.partner = Partner.objects.create(name='Potato Company', description='Potato company')
        self.assignment = CourseAssignment.objects.create(
            user=self.student_user, course=self.course, group_time=CourseAssignment.EARLY)

        self.started_working_at = StudentStartedWorkingAt.objects.create(assignment=self.assignment,
                                       partner=self.partner,
                                       partner_name=self.partner.name)

    def test_unicode(self):
        expected = '{} - {}'.format(self.assignment, self.partner)
        self.assertEqual(expected, unicode(self.started_working_at))


class SolutionTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
        )

        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.github_account = 'https://github.com/Ivaylo-Bachvarov'
        self.student_user.save()

        self.partner_potato = Partner.objects.create(
            name='Potato Company', description='Potato company')
        self.partner_salad = Partner.objects.create(
            name='Salad Company', description='Salad Company')

        self.hr_user = User.objects.create_user('ivan_hr@gmail.com', '1234')
        self.hr_user.status = User.HR
        self.hr_user.hr_of = self.partner_potato
        self.hr_user.save()

        self.assignment = CourseAssignment.objects.create(
            user=self.student_user, course=self.course, group_time=CourseAssignment.EARLY)
        self.assignment.favourite_partners.add(self.partner_potato)
        self.third_wheel = User.objects.create_user('third_wheel@gmail.com', '456')

        self.green_task = Task.objects.create(
            name='Green task',
            course=self.course,
        )
        self.task_url = 'https://github.com/HackBulgaria/Frontend-JavaScript-1/tree/master/week1/2-jQuery-Gauntlet'
        self.task = Task.objects.create(course=self.course, description=self.task_url, name='<2> jQuery-Gauntlet')
        self.solution_url = 'https://github.com/syndbg/HackBulgaria/'
        self.solution = Solution.objects.create(task=self.task, user=self.student_user, repo=self.solution_url)

    def test_get_user_github_username(self):
        self.assertEqual('Ivaylo-Bachvarov', self.solution.get_user_github_username())

    def test_get_github_user_and_repo_names(self):
        result = self.solution.get_github_user_and_repo_names()
        self.assertEqual('syndbg', result['user_name'])
        self.assertEqual('HackBulgaria', result['repo_name'])
        self.solution.repo = 'https://github.com/syndbg/'

        result = self.solution.get_github_user_and_repo_names()
        self.assertEqual('syndbg', result['user_name'])
        self.assertEqual('', result['repo_name'])
