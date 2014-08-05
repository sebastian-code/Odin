from django.utils import unittest
from django.test import TestCase
from django.test.client import Client
from .models import CheckIn, User, HrLoginLog, CourseAssignment, Solution
from courses.models import Partner, Course
from django.conf import settings
from django.core.urlresolvers import reverse
from courses.models import Task

import datetime
client = Client()


class CheckInCase(unittest.TestCase):

    def setUp(self):
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

    def tearDown(self):
        self.student_user.delete()
        self.hr_user.delete()

    def test_new_check_in_status(self):
        response = client.post('/set-check-in/', {
            'mac': self.student_user.mac,
            'token': self.checkin_settings,
        })

        self.assertEqual(response.status_code, 200)

    def test_new_check_in_result(self):
        response = client.post('/set-check-in/', {
            'mac': self.student_user.mac,
            'token': self.checkin_settings,
        })

        checkin = CheckIn.objects.get(student=self.student_user)

        assert checkin is not None

    def test_new_check_in_case_insensitive(self):
        response = client.post('/set-check-in/', {
            'mac': self.student_user.mac,
            'token': self.checkin_settings,
        })

        checkin = CheckIn.objects.get(student=self.student_user)

        assert checkin is not None

    def test_double_checkin_same_day(self):
        response_first = client.post('/set-check-in/', {'mac': self.student_user.mac,
                                                        'token': self.checkin_settings,
                                                        })

        response_second = client.post('/set-check-in/', {'mac': self.student_user.mac,
                                                         'token': self.checkin_settings,
                                                         })

        self.assertEqual(response_first.status_code, 200)
        self.assertEqual(response_second.status_code, 418)

    def test_hr_login_log(self):
        before_log = HrLoginLog.objects.count()
        client.login(username='ivan_hr@gmail.com', password='1234')
        after_log = HrLoginLog.objects.count()

        self.assertEqual(before_log + 1, after_log)


class CourseAssignmentTest(TestCase):
<<<<<<< HEAD

=======
        def setUp(self):
            self.course = Course.objects.create(
                name='Test Course',
                url='test-course',
                application_until=datetime.datetime.now(),
            )

            self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
            self.student_user.status = User.STUDENT
            self.student_user.save()

            self.partner_potato = Partner.objects.create(name='Potato Company', description='Potato company')
            self.partner_salad = Partner.objects.create(name='Salad Company', description='Salad Company')

            self.hr_user = User.objects.create_user('ivan_hr@gmail.com', '1234')
            self.hr_user.status = User.HR
            self.hr_user.hr_of = self.partner_potato
            self.hr_user.save()

            self.assignment = CourseAssignment.objects.create(user=self.student_user, course=self.course, group_time=CourseAssignment.EARLY)
            self.assignment.favourite_partners.add(self.partner_potato)
            self.third_wheel = User.objects.create_user('third_wheel@gmail.com', '456')

        def tearDown(self):
            self.course.delete()
            self.student_user.delete()
            self.partner_potato.delete()
            self.partner_salad.delete()
            self.hr_user.delete()
            self.assignment.delete()
            self.third_wheel.delete()

        def test_create_a_new_assignment(self):
            self.client = Client();
            self.client.login(username='ivo_student@gmail.com', password='123')
            response = self.client.get(reverse('students:assignment', kwargs={'id':self.assignment.id}))
            self.assertEqual(200, response.status_code)

        def test_email_field_visibility_when_partner_hr(self):
            self.client = Client();
            self.client.login(username='ivan_hr@gmail.com', password='1234')
            response = self.client.get(reverse('students:assignment', kwargs={'id':self.assignment.id}))
            self.assertContains(response, self.assignment.user.email)

        def test_email_field_visibility_when_non_partner_hr(self):
            self.client = Client();
            self.client.login(username='third_wheel@gmail.com', password='456')
            response = self.client.get(reverse('students:assignment', kwargs={'id':self.assignment.id}))
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
        self.assignment = CourseAssignment.objects.create(
            user=self.student_user,
            course=self.course,
            group_time=CourseAssignment.EARLY
        )

        self.green_task = Task.objects.create(
            name="Green task",
            course=self.course,
        )

    def tearDown(self):
        self.course.delete()
        self.student_user.delete()
        self.partner_potato.delete()
        self.partner_salad.delete()
        self.hr_user.delete()
        self.assignment.delete()
        self.third_wheel.delete()

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
        self.assignment.delete()
        self.green_task.delete()

    def test_add_solution_get_status(self):
        self.client = Client();
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:add-solution'))
        self.assertEqual(405, response.status_code)

    def test_add_solution_not_existing_task(self):
        self.client = Client();
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
        self.client = Client();
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
