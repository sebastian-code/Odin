import datetime
import os
import unittest

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.core.validators import ValidationError
from django.db import IntegrityError
from django.test import TestCase

import mock
from github import GithubException

from .models import CheckIn, User, HrLoginLog, CourseAssignment, Solution, StudentStartedWorkingAt
from courses.models import Partner, Course, Task
from management.commands.generate_certificates import is_new_valid_github_account
from management.commands.helpers.classes import TempCertificate, GithubSolution


class UserViewsTest(TestCase):

    def setUp(self):
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.save()

    def test_login_when_already_logged_in(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.post('/login', {'username': 'ivo_student@gmail.com', 'password': '123'})
        self.assertEqual(301, response.status_code)
        self.assertTemplateUsed('profile.html', response)

    def test_login_when_not_logged_in(self):
        response = self.client.post('/login', {'username': 'ivo_student@gmail.com', 'password': '123'})
        self.assertEqual(301, response.status_code)
        self.assertTemplateUsed('login_form.html')

    def test_logout_when_not_logged_in(self):
        response = self.client.post('/logout')
        self.assertEqual(301, response.status_code)
        self.assertTemplateUsed('login_form.html', response)

    def test_logout_when_logged_in(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.post('/logout')
        self.assertEqual(301, response.status_code)
        self.assertTemplateUsed('index.html', response)


class CheckInCaseViewsTest(TestCase):

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

    def test_new_check_in(self):
        response = self.client.post('/set-check-in/', {
            'mac': self.student_user.mac,
            'token': self.checkin_settings,
        })
        checkin = CheckIn.objects.get(student=self.student_user)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(checkin)

    def test_new_check_in_case_insensitive(self):
        response = self.client.post('/set-check-in/', {
            'mac': self.student_user.mac,
            'token': self.checkin_settings,
        })
        checkin = CheckIn.objects.get(student=self.student_user)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(checkin)

    def test_double_checkin_same_day(self):
        response_first = self.client.post('/set-check-in/', {'mac': self.student_user.mac,
                                                             'token': self.checkin_settings,
                                                             })

        response_second = self.client.post('/set-check-in/', {'mac': self.student_user.mac,
                                                              'token': self.checkin_settings,
                                                              })

        self.assertEqual(response_first.status_code, 200)
        self.assertIsNotNone(response_first)
        self.assertEqual(response_second.status_code, 418)
        self.assertIsNotNone(response_second)

    def test_hr_login_log(self):
        before_log = HrLoginLog.objects.count()
        self.client.login(username='ivan_hr@gmail.com', password='1234')
        after_log = HrLoginLog.objects.count()

        self.assertEqual(before_log + 1, after_log)

class CourseAssignmentViewsTest(TestCase):

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

    def test_vote_for_partner_form_visibility_when_not_ask_for_favorite_partner(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertNotContains(response, 'data-reveal-id="vote-for-partner"')

    def test_vote_for_partner_form_visibility_when_ask_for_favorite_partner(self):
        self.course.ask_for_favorite_partner = True
        self.course.save()
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertContains(response, 'data-reveal-id="vote-for-partner')

    def test_give_feedback_form_visibility_when_not_ask_for_feedback(self):
        self.course.ask_for_feedback = False
        self.course.save()
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertNotContains(response, 'data-reveal-id="give-feedback"')

    def test_give_feedback_form_visibility_when_course_end_time_is_none(self):
        self.course.end_time = None
        self.course.save()
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertContains(response, 'data-reveal-id="give-feedback"', count=1)

    @mock.patch('students.views.datetime')
    def test_give_feedback_form_visibility_when_course_has_not_ended(self, mocked_datetime):
        mocked_datetime.date = mock.Mock()
        mocked_datetime.date.today = mock.Mock(return_value=datetime.date(2000, 1, 1))
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertNotContains(response, 'data-reveal-id="give-feedback"')

    @mock.patch('students.views.datetime')
    def test_give_feedback_form_visiblity_when_course_has_ended(self, mocked_datetime):
        mocked_datetime.date = mock.Mock()
        mocked_datetime.date.today = mock.Mock(return_value=self.course.end_time + datetime.timedelta(days=7))
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertContains(response, 'data-reveal-id="give-feedback"')

    def test_give_feedback_form_visibility_when_has_not_started_working_at(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertContains(response, 'data-reveal-id="give-feedback"')

    def test_give_feedback_form_visibility_when_has_started_working_at(self):
        StudentStartedWorkingAt.objects.create(assignment=self.assignment,
                                               partner=self.partner_potato,
                                               partner_name=self.partner_potato.name)
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertNotContains(response, 'data-reveal-id="give-feedback"')

    def test_create_a_new_assignment(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(
            reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('assignment.html', response)

    def test_email_field_visibility_when_partner_hr(self):
        self.client.login(username='ivan_hr@gmail.com', password='1234')
        response = self.client.get(
            reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertContains(response, self.assignment.user.email)
        self.assertTemplateUsed('assignment.html', response)

    def test_email_field_visibility_when_non_partner_hr(self):
        self.client.login(username='third_wheel@gmail.com', password='456')
        response = self.client.get(
            reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertNotContains(response, self.assignment.user.email)
        self.assertTemplateUsed('assignment.html', response)


class SolutionViewsTest(TestCase):

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

    def test_email_field_visibility_when_partner_hr(self):
        self.client.login(username='ivan_hr@gmail.com', password='1234')
        response = self.client.get(
            reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, self.assignment.user.email)
        self.assertTemplateUsed('assignment.html', response)

    def test_email_field_visibility_when_non_partner_hr(self):
        self.client.login(username='third_wheel@gmail.com', password='456')
        response = self.client.get(
            reverse('students:assignment', kwargs={'id': self.assignment.id}))
        self.assertNotContains(response, self.assignment.user.email)
        self.assertTemplateUsed('assignment.html', response)

    def test_add_solution_get_status(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:add_solution'))
        self.assertEqual(405, response.status_code)

    def test_add_solution_not_existing_task(self):
        before_adding = Solution.objects.count()
        self.client.login(username='ivo_student@gmail.com', password='123')

        response = self.client.post(reverse('students:add_solution'),
                                    {
            'task': 3777,
            'repo': 'https://github.com/HackBulgaria/Odin',
        })
        after_adding = Solution.objects.count()
        self.assertEqual(before_adding, after_adding)
        self.assertEqual(422, response.status_code)

    def test_add_solution_status_code(self):
        self.client.login(username='ivo_student@gmail.com', password='123')

        before_adding = Solution.objects.count()
        response = self.client.post(reverse('students:add_solution'),
                                    {
            'task': self.green_task.id,
            'repo': 'https://github.com/HackBulgaria/Odin',
        })
        after_adding = Solution.objects.count()

        self.assertEqual(before_adding + 1, after_adding)
        self.assertEqual(200, response.status_code)

    def test_edit_solution(self):
        self.client.login(username='ivo_student@gmail.com', password='123')

        before_adding = Solution.objects.count()
        response = self.client.post(reverse('students:add_solution'),
                                    {
            'task': self.green_task.id,
            'repo': 'https://github.com/HackBulgaria/Odin',
        })

        response = self.client.post(reverse('students:add_solution'),
                                    {
            'task': self.green_task.id,
            'repo': 'https://github.com/HackBulgaria/Odin2',
        })

        after_adding = Solution.objects.count()

        self.assertEqual(before_adding + 1, after_adding)
        self.assertEqual(200, response.status_code)


class API_Tests(TestCase):

    def setUp(self):
        self.checkin_settings = '123'
        settings.CHECKIN_TOKEN = self.checkin_settings

        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
        )

        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.mac = '4c:80:93:1f:a4:50'
        self.student_user.status = User.STUDENT
        self.student_user.github_account = 'https://github.com/Ivaylo-Bachvarov'
        self.student_user.save()

    def test_api_students_with_no_checkins(self):
        expected = '[{"available": false, "courses": [], "github": "https://github.com/Ivaylo-Bachvarov", "name": ""}]'
        response = self.client.get('/api/students/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.content)

    def test_api_students_with_checkins(self):
        expected = '[{"available": true, "courses": [], "github": "https://github.com/Ivaylo-Bachvarov", "name": ""}]'
        self.client.post('/set-check-in/', {
            'mac': self.student_user.mac,
            'token': self.checkin_settings,
        })
        response = self.client.get('/api/students/')
        self.assertEqual(expected, response.content)

    def test_api_checkins_with_none_checked_in(self):
        response = self.client.get('/api/checkins/')
        self.assertEqual(200, response.status_code)
        self.assertEqual('[]', response.content)

    def test_api_checkins_with_checked_in(self):
        self.client.post('/set-check-in/', {
            'mac': self.student_user.mac,
            'token': self.checkin_settings,
        })
        response = self.client.get('/api/checkins/')
        date_str = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        expected = [{"date": date_str, "student_id": self.student_user.id, "student_courses": [], "student_name": ''}]
        expected = "{}".format(expected).replace("'", '"')
        self.assertEqual(expected, response.content)
