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
from validators import validate_mac, validate_url, validate_github, validate_linkedin


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


class UserTest(TestCase):

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


class CheckInCaseTest(TestCase):

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


class CourseAssignmentTest(TestCase):

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


class GetCommandsTest(TestCase):
    def setUp(self):
        self.filename = 'students.txt'
        self.user_without_github = User.objects.create_user('asd@gmail.com', '123')
        self.user_without_github.first_name = 'Asd'
        self.user_without_github.save()

        self.user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.user.first_name = 'Ivo'
        self.user.status = User.STUDENT
        self.user.github_account = 'https://github.com/Ivaylo-Bachvarov'
        self.user.save()

    def tearDown(self):
        os.remove(self.filename)

    def test_get_people_with_no_github(self):
        expected = '[1] {} - {}\n'.format(self.user_without_github.first_name, self.user_without_github.email)
        call_command('get_people_with_no_github', self.filename)
        with open(self.filename, 'r') as f:
            actual = f.read()
        self.assertEqual(expected, actual)

    def test_get_github_accounts(self):
        expected = '{} - {} - {}\n'.format(self.user.first_name, self.user.email, self.user.github_account)
        call_command('get_github_accounts', self.filename)
        with open(self.filename, 'r') as f:
            actual = f.read()
        self.assertEqual(expected, actual)


class GenerateCertificateTest(TestCase):
    def setUp(self):
        self.github_parameters = {'user_name': 'syndbg', 'repo_name': 'atom'}
        self.visited_repos = [{'user_name': 'kennethreitz', 'repo_name': 'requests'}, {'user_name': 'django', 'repo_name': 'django'}]

    def test_is_new_valid_github_account(self):
        existing_parameters = {'user_name': 'kennethreitz', 'repo_name': 'requests'}
        self.assertFalse(is_new_valid_github_account(existing_parameters, self.visited_repos))
        self.assertTrue(is_new_valid_github_account(self.github_parameters, self.visited_repos))

    def test_generate_certificate(self):
        pass


class TempCertificateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('certificate@gmaaail.com', '123')
        self.user.github_account = 'https://github.com/syndbg'
        self.user.save()

        self.start_time = datetime.date.today() - datetime.timedelta(days=7)
        self.end_time = datetime.date.today()
        self.user = User.objects.create()
        self.course = Course.objects.create(
            name='Certificate Course',
            url='certificate-course',
            application_until=datetime.datetime.now(),
            start_time=self.start_time,
            end_time=self.end_time
        )
        self.assignment = CourseAssignment.objects.create(
            user=self.user, course=self.course, group_time=CourseAssignment.EARLY)
        self.temp_certificate = TempCertificate(self.assignment)

    def test_set_start_time(self):
        self.assertEqual(self.start_time, self.temp_certificate.start_time)

    def test_set_end_time(self):
        expected = self.end_time + datetime.timedelta(days=31)
        self.assertEqual(expected, self.temp_certificate.end_time)

    def test_get_total_commits(self):
        self.assertEqual(0, self.temp_certificate.get_total_commits())

    def test_update_stats(self):
        self.assertEqual(0, self.temp_certificate.open_issues)
        self.assertEqual(0, self.temp_certificate.closed_issues)
        api_stats_dictionary = {'open_issues': 5, 'closed_issues': 3}
        self.temp_certificate.update_stats(api_stats_dictionary)
        self.assertEqual(5, self.temp_certificate.open_issues)
        self.assertEqual(3, self.temp_certificate.closed_issues)

    def test_add_cheated_solution(self):
        task_url = 'https://github.com/HackBulgaria/Frontend-JavaScript-1/tree/master/week1/2-jQuery-Gauntlet'
        task = Task.objects.create(course=self.course, description=task_url, name='<2> jQuery-Gauntlet')
        solution_url = 'https://github.com/syndbg/HackBulgaria/'
        solution = Solution.objects.create(task=task, user=self.user, repo=solution_url)
        self.temp_certificate.add_cheated_solution(solution)
        self.assertTrue(self.temp_certificate.has_cheated)
        self.assertIn(solution, self.temp_certificate.cheated_solutions)

    def test_save_weekly_commit_in_db(self):
        pass

    def test_log_cheating(self):
        pass

    def test_save_certificate_in_db(self):
        pass

    def test_log_or_save_in_db(self):
        pass


class GithubSolutionTest(TestCase):

    def setUp(self):
        self.start_time = datetime.date.today() - datetime.timedelta(days=7)
        self.end_time = datetime.date.today()
        self.user = User.objects.create_user('certificate@gmail.com', '123')
        self.user.github_account = 'https://github.com/syndbg'
        self.user.save()
        self.course = Course.objects.create(
            name='Certificate Course',
            url='certificate-course',
            start_time=self.start_time,
            application_until=datetime.datetime.now(),
            end_time=self.end_time
        )
        task_url = 'https://github.com/HackBulgaria/Frontend-JavaScript-1/tree/master/week1/2-jQuery-Gauntlet'
        task = Task.objects.create(course=self.course, description=task_url, name='<2> jQuery-Gauntlet')
        solution_url = 'https://github.com/syndbg/HackBulgaria/'
        self.solution = Solution.objects.create(task=task, user=self.user, repo=solution_url)

        self.username = 'syndbg'
        self.repo_name = 'HackBulgaria'
        self.github_solution = GithubSolution(self.username, self.repo_name, self.solution)

    def test_set_api_repo(self):
        pass

    def test_is_invalid_repo(self):
        pass

    def test_is_cheating(self):
        pass

    def test_is_fork(self):
        pass

    def test_update_commits_count(self):
        pass

    def test_get_commits_count(self):
        self.assertEqual(0, self.github_solution.get_commits_count())

    def test_count_commits(self):
        pass

    def test_get_closed_issues_count(self):
        pass

    def test_get_stats(self):
        pass
