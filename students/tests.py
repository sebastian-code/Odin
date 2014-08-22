import datetime
import unittest

from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import ValidationError
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password

from courses.models import Partner, Course, Task
from validators import validate_mac, validate_url, validate_github, validate_linkedin
from .models import CheckIn, User, HrLoginLog, CourseAssignment, Solution


class UserManagerTest(TestCase):
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


class CheckInCaseTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.checkin_settings = '123'
        settings.CHECKIN_TOKEN = self.checkin_settings

        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.mac = '4c:80:93:1f:a4:50'
        self.student_user.save()

        self.hr_user = User.objects.create_user('ivan_hr@gmail.com', '1234')
        self.hr_user.status = User.HR
        self.hr_user.mac = '4c:80:93:1f:a4:51'
        self.hr_user.save()

    def test_new_check_in_status(self):
        response = self.client.post('/set-check-in/', {
            'mac': self.student_user.mac,
            'token': self.checkin_settings,
        })
        self.assertEqual(response.status_code, 200)

    def test_new_check_in_result(self):
        response = self.client.post('/set-check-in/', {
            'mac': self.student_user.mac,
            'token': self.checkin_settings,
        })
        checkin = CheckIn.objects.get(student=self.student_user)
        self.assertIsNotNone(checkin)

    def test_new_check_in_case_insensitive(self):
        response = self.client.post('/set-check-in/', {
            'mac': self.student_user.mac,
            'token': self.checkin_settings,
        })
        checkin = CheckIn.objects.get(student=self.student_user)
        self.assertIsNotNone(checkin)

    def test_double_checkin_same_day(self):
        response_first = self.client.post('/set-check-in/', {'mac': self.student_user.mac,
                                                             'token': self.checkin_settings,
                                                             })

        response_second = self.client.post('/set-check-in/', {'mac': self.student_user.mac,
                                                              'token': self.checkin_settings,
                                                              })

        self.assertEqual(response_first.status_code, 200)
        self.assertEqual(response_second.status_code, 418)

    def test_hr_login_log(self):
        before_log = HrLoginLog.objects.count()
        self.client.login(username='ivan_hr@gmail.com', password='1234')
        after_log = HrLoginLog.objects.count()

        self.assertEqual(before_log + 1, after_log)


class CourseAssignmentTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
        )

        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
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

    def test_create_a_new_assignment(self):
        self.client = Client()
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(
            reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertEqual(200, response.status_code)

    def test_email_field_visibility_when_partner_hr(self):
        self.client = Client()
        self.client.login(username='ivan_hr@gmail.com', password='1234')
        response = self.client.get(
            reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertContains(response, self.assignment.user.email)

    def test_email_field_visibility_when_non_partner_hr(self):
        self.client = Client()
        self.client.login(username='third_wheel@gmail.com', password='456')
        response = self.client.get(
            reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertNotContains(response, self.assignment.user.email)


class SolutionTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
        )

        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
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

        self.green_task = Task.objects.create(
            name="Green task",
            course=self.course,
        )

    def test_create_a_new_assignment(self):
        self.client = Client()
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(
            reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertEqual(200, response.status_code)

    def test_email_field_visibility_when_partner_hr(self):
        self.client = Client()
        self.client.login(username='ivan_hr@gmail.com', password='1234')
        response = self.client.get(
            reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertContains(response, self.assignment.user.email)

    def test_email_field_visibility_when_non_partner_hr(self):
        self.client = Client()
        self.client.login(username='third_wheel@gmail.com', password='456')
        response = self.client.get(
            reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertNotContains(response, self.assignment.user.email)

    def test_add_solution_get_status(self):
        self.client = Client()
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:add-solution'))
        self.assertEqual(405, response.status_code)

    def test_add_solution_not_existing_task(self):
        self.client = Client()
        before_adding = Solution.objects.count()
        self.client.login(username='ivo_student@gmail.com', password='123')

        response = self.client.post(reverse('students:add-solution'),
                                    {
            'task': 3,
            'repo': 'https://github.com/HackBulgaria/Odin',
        })

        after_adding = Solution.objects.count()
        self.assertEqual(before_adding, after_adding)
        self.assertEqual(422, response.status_code)

    def test_add_solution_status_code(self):
        self.client = Client()
        self.client.login(username='ivo_student@gmail.com', password='123')

        before_adding = Solution.objects.count()
        response = self.client.post(reverse('students:add-solution'),
                                    {
            'task': self.green_task.id,
            'repo': 'https://github.com/HackBulgaria/Odin',
        })
        after_adding = Solution.objects.count()

        self.assertEqual(before_adding + 1, after_adding)
        self.assertEqual(200, response.status_code)

    def test_edit_solution(self):
        self.client = Client()
        self.client.login(username='ivo_student@gmail.com', password='123')

        before_adding = Solution.objects.count()
        response = self.client.post(reverse('students:add-solution'),
                                    {
            'task': self.green_task.id,
            'repo': 'https://github.com/HackBulgaria/Odin',
        })

        response = self.client.post(reverse('students:add-solution'),
                                    {
            'task': self.green_task.id,
            'repo': 'https://github.com/HackBulgaria/Odin2',
        })

        after_adding = Solution.objects.count()

        self.assertEqual(before_adding + 1, after_adding)
        self.assertEqual(200, response.status_code)


class ValidatorsTest(unittest.TestCase):

    def test_validate_mac(self):
        invalid_mac = ':ez:77:b4:14:66:b'
        self.assertRaises(ValidationError, validate_mac, invalid_mac)
        valid_mac = 'bd:88:d0:19:63:c9'
        self.assertIsNone(validate_mac(valid_mac))

    def test_validate_url(self):
        invalid_url = '%invalid%[/]*url.com'
        self.assertRaises(ValidationError, validate_url, invalid_url, 'github', 'invalid url given', 'invalid_url')
        valid_url = 'http://hackbulgaria.com'
        self.assertIsNone(validate_url(valid_url, 'hackbulgaria.com', 'invalid url given', 'invalid_url'))

    def test_validate_github(self):
        invalid_url = 'http://facebook.com'
        self.assertRaises(ValidationError, validate_github, invalid_url)
        valid_url = 'https://github.com/HackBulgaria/Odin'
        self.assertIsNone(validate_github(valid_url))

    def test_validate_linkedin(self):
        invalid_url = 'http://facebook.com'
        self.assertRaises(ValidationError, validate_linkedin, invalid_url)
        valid_url = 'https://www.linkedin.com/in/jeffweiner08gst'  # Linkedin CEO
        self.assertIsNone(validate_linkedin(valid_url))
