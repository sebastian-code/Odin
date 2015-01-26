import datetime
import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

import mock

from courses.models import Partner, Course, Task
from students.models import CheckIn, User, HrLoginLog, CourseAssignment, Solution, StudentStartedWorkingAt


class UserViewsTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
            end_time=datetime.date.today(),
            ask_for_feedback=False
        )
        self.teacher_user = User.objects.create_user('teacher@teacher.com', 'teach')
        self.teacher_user.status = User.TEACHER
        self.teacher_user.save()

        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.save()

        self.partner_potato = Partner.objects.create(name='Potato Company', description='Potato company')
        self.partner_salad = Partner.objects.create(name='Salad Company', description='Salad Company')

        self.hr_user = User.objects.create_user('ivan_hr@gmail.com', '1234')
        self.hr_user.status = User.HR
        self.hr_user.save()

        self.student_assignment = CourseAssignment.objects.create(
            user=self.student_user, course=self.course, group_time=CourseAssignment.EARLY)
        self.teacher_assignment = CourseAssignment.objects.create(
            user=self.teacher_user, course=self.course, group_time=CourseAssignment.EARLY)
        self.hr_assignment = CourseAssignment.objects.create(
            user=self.hr_user, course=self.course, group_time=CourseAssignment.EARLY)

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

    def test_user_profile_correct_url_and_template_used(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:user_profile'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('profile.html', response)

    def test_user_profile_has_submitted_solutions_button_when_teacher(self):
        self.client.login(username='teacher@teacher.com', password='teach')
        response = self.client.get(reverse('students:user_profile'))

        submitted_solutions_url = reverse('courses:show_submitted_solutions', kwargs={'course_url': self.course.url})
        self.assertContains(response, submitted_solutions_url)

    def test_user_profile_has_show_course_students_button_when_hr(self):
        self.client.login(username='ivan_hr@gmail.com', password='1234')
        response = self.client.get(reverse('students:user_profile'))

        show_course_students_url = reverse('courses:show_course_students', kwargs={'course_url': self.course.url})
        self.assertContains(response, show_course_students_url)

    def test_edit_profile_http_post(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.post(reverse('students:edit_profile'))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('students:user_profile'))
        self.assertTemplateUsed('assignment.html')

    def test_edit_profile_http_get(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:edit_profile'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('edit_profile.html', response)


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

    def test_set_checkin_when_checkin_token_differs(self):
        response = self.client.post('/set-check-in/', {
            'mac': self.student_user.mac,
            'token': '456',
        })
        self.assertEqual(511, response.status_code)

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
        self.assertEqual(after_log, before_log + 1)


class CourseAssignmentViewsTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
            end_time=datetime.date.today(),
            ask_for_feedback=True
        )
        self.teacher_user = User.objects.create_user('teacher@teacher.com', 'teach')
        self.teacher_user.status = User.TEACHER
        self.teacher_user.save()

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

        self.teacher_assignment = CourseAssignment.objects.create(user=self.teacher_user,
                                                                  course=self.course,
                                                                  group_time=CourseAssignment.EARLY)

    def test_vote_for_partner_form_visibility_when_not_ask_for_favorite_partner(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:user_profile'))
        self.assertNotContains(response, r'data-reveal-id="vote-for-partner-1')

    def test_vote_for_partner_form_visibility_when_ask_for_favorite_partner(self):
        self.course.ask_for_favorite_partner = True
        self.course.save()
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:user_profile'))
        self.assertContains(response, r'data-reveal-id="vote-for-partner-1')

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

    def test_assignment_when_user_is_a_teacher(self):
        self.client.login(username='teacher@teacher.com', password='teach')
        response = self.client.get(reverse('students:assignment', kwargs={'id': self.teacher_assignment.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('assignment.html', response)
        self.assertTrue('notes' in response.context)
        self.assertTrue('form' in response.context)

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

    def test_toggle_assignment_activity_only_visible_to_teachers(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:assignment', kwargs={'id': self.assignment.id}))

        activity_switch = 'id="activity_switch"'
        self.assertNotContains(response, activity_switch)

    def test_toggle_assignment_activity_OKs_when_teacher(self):
        self.client.login(username='teacher@teacher.com', password='teach')
        assignment_id = self.teacher_assignment.id
        response = self.client.post(reverse('students:toggle_assignment_activity'), {'id': assignment_id})
        assignment = CourseAssignment.objects.get(id=assignment_id)

        self.assertEqual(200, response.status_code)
        self.assertFalse(assignment.is_attending)

    def test_toggle_assignment_activity_FORBIDS_when_not_teacher(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        assignment_id = self.teacher_assignment.id
        response = self.client.post(reverse('students:toggle_assignment_activity'), {'id': assignment_id})
        assignment = CourseAssignment.objects.get(id=assignment_id)

        self.assertEqual(403, response.status_code)
        self.assertTrue(assignment.is_attending)


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

    # TODO: Fix this after students.tests.test_forms is rewritten.
    # Currently this is a forms issue that we try to fix in views. This is wrong.
    # def test_edit_solution(self):
    #     self.client.login(username='ivo_student@gmail.com', password='123')

    #     before_adding = Solution.objects.count()
    #     response = self.client.post(reverse('students:add_solution'),
    #                                 {
    #         'task': self.green_task.id,
    #         'repo': 'https://github.com/HackBulgaria/Odin',
    #     })

    #     response = self.client.post(reverse('students:add_solution'),
    #                                 {
    #         'task': self.green_task.id,
    #         'repo': 'https://github.com/HackBulgaria/Odin2',
    #     })

    #     after_adding = Solution.objects.count()

    #     self.assertEqual(before_adding + 1, after_adding)
    #     self.assertEqual(200, response.status_code)

    def test_view_solutions(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('students:solutions', kwargs={'course_url': self.course.url}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('solutions.html', response)


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
        expected = [
            {
                "available": False,
                "courses": [],
                "github": "https://github.com/Ivaylo-Bachvarov",
                "name": ""
            }
        ]
        response = self.client.get('/api/students/')
        result = json.loads(response.content.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, result)

    def test_api_students_with_checkins(self):
        expected = [
            {
                "available": True,
                "courses": [],
                "github": "https://github.com/Ivaylo-Bachvarov", "name": ""
            }
        ]

        self.client.post('/set-check-in/', {
            'mac': self.student_user.mac,
            'token': self.checkin_settings,
        })
        response = self.client.get('/api/students/')
        result = json.loads(response.content.decode())

        self.assertEqual(expected, result)

    def test_api_checkins_with_none_checked_in(self):
        response = self.client.get('/api/checkins/')
        self.assertEqual(200, response.status_code)
        self.assertEqual('[]', response.content.decode())

    def test_api_checkins_with_checked_in(self):
        self.client.post('/set-check-in/', {
            'mac': self.student_user.mac,
            'token': self.checkin_settings,
        })
        response = self.client.get('/api/checkins/')
        date_str = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        expected = [
            {
                "date": date_str,
                "student_id": self.student_user.id,
                "student_courses": [],
                "student_name": ''
            }
        ]
        result = json.loads(response.content.decode())

        self.assertEqual(expected, result)
