from datetime import datetime

from django.utils import timezone
from django.core.urlresolvers import reverse
from django.test import TestCase

from applications.forms import ApplicationForm, AddApplicationSolutionForm, ExistingUserApplicationForm, ExistingAttendingUserApplicationForm
from applications.models import Application, ApplicationSolution, ApplicationTask
from applications.views import NO_COURSES_TO_APPLY_FOR_ERROR, HASNT_ATTENDED_LAST_ENROLLED_COURSE_ERROR, HAS_ATTENDED_LAST_ENROLLED_COURSE_MESSAGE, ALREADY_ADMITTED_IN_COURSE_ERROR, ALREADY_APPLIED_FOR_COURSE_ERROR
from courses.models import Course, Partner
from students.models import CourseAssignment, EducationInstitution, User


class ApplicationViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='user@user.com', password='123')
        self.education = EducationInstitution.objects.create(name='MIT')
        self.given_name = 'One Two'
        self.given_email = 'foo@bar.com'
        self.given_github = 'https://github.com/HackBulgaria/Odin'
        self.given_linkedin = 'https://www.linkedin.com/'

    # TODO: Figure out why Django insists on adding a Course object from nowhere?
    # def test_apply_when_no_courses_to_apply_for(self):
    #     response = self.client.get(reverse('applications:apply'))
    #     self.assertIsInstance(response.context['form'], ApplicationForm)
    #     self.assertIsNone(response.context['latest_assignment'])
    #     self.assertEqual(NO_COURSES_TO_APPLY_FOR_ERROR, response.context['error_message'])
    #     self.assertTemplateUsed(200, response.status_code)
    #     self.assertTemplateUsed('generic_error.html', response)

    def test_apply_when_anonymous_user(self):
        course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
        )
        response = self.client.get(reverse('applications:apply'))
        self.assertIsNone(response.context['latest_assignment'])
        self.assertIsInstance(response.context['form'], ApplicationForm)
        self.assertTemplateUsed(200, response.status_code)
        self.assertTemplateUsed('apply.html', response)

        users_count_before = User.objects.count()
        applications_count_before = Application.objects.count()
        apply_response = self.client.post(reverse('applications:apply'), {'course': course.pk, 'name': self.given_name, 'email': self.given_email,
                                                                          'education': self.education.pk, 'skype': 'foobar', 'phone': '007',
                                                                          'linkedin_account': self.given_linkedin, 'github_account': self.given_github})
        applications_count_after = Application.objects.count()
        users_count_after = User.objects.count()

        self.assertEqual(302, apply_response.status_code)
        self.assertTemplateUsed('thanks.html', apply_response)
        self.assertEqual(
            applications_count_before + 1, applications_count_after)
        self.assertEqual(users_count_before + 1, users_count_after)

    # TODO: Figure out why again a course comes out from nowhere.
    # And the course created in the test isn't actually in the database
    # def test_apply_when_already_admitted(self):
    #     course = Course.objects.create(
    #         name='Test Course',
    #         url='test-course',
    #         application_until=timezone.now(),
    #     )
    #     CourseAssignment.objects.create(
    #         user=self.user, course=course, group_time=1)
    #     self.client.login(username='user@user.com', password='123')
    #     response = self.client.get(reverse('applications:apply'))

    #     self.assertEqual(ALREADY_ADMITTED_IN_COURSE_ERROR.format(
    #         course.name), response.context['error_message'])
    #     self.assertEqual(200, response.status_code)
    #     self.assertTemplateUsed('generic_error.html', response)

    def test_apply_when_already_applied(self):
        course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
        )
        Application.objects.create(course=course, student=self.user)
        self.client.login(username='user@user.com', password='123')
        response = self.client.get(reverse('applications:apply'))

        self.assertEqual(ALREADY_APPLIED_FOR_COURSE_ERROR.format(
            course.name), response.context['error_message'])
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('generic_error.html', response)

    def test_apply_when_registered_user_with_no_assignments(self):
        course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
        )
        self.client.login(username='user@user.com', password='123')
        response = self.client.get(reverse('applications:apply'))

        self.assertIsNone(response.context['latest_assignment'])
        self.assertIsInstance(
            response.context['form'], ExistingUserApplicationForm)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('apply.html', response)

        users_count_before = User.objects.count()
        applications_count_before = Application.objects.count()
        apply_response = self.client.post(reverse('applications:apply'), {'course': course.pk, 'name': self.given_name, 'email': self.given_email,
                                                                          'education': self.education.pk, 'skype': 'foobar', 'phone': '007',
                                                                          'linkedin_account': self.given_linkedin, 'github_account': self.given_github})
        applications_count_after = Application.objects.count()
        users_count_after = User.objects.count()

        self.assertEqual(302, apply_response.status_code)
        self.assertTemplateUsed('thanks.html', apply_response)
        self.assertEqual(
            applications_count_before + 1, applications_count_after)
        self.assertEqual(users_count_before, users_count_after)

    def test_apply_when_user_who_didnt_attend_last_course_he_applied_for(self):
        course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
        )
        expired_course = Course.objects.create(
            name='Expired Course',
            url='expired-course',
            application_until=datetime(1900, 1, 1),
        )
        CourseAssignment.objects.create(course=expired_course, user=self.user,
                                        group_time=1, is_attending=False)
        self.client.login(username='user@user.com', password='123')
        response = self.client.get(reverse('applications:apply'))
        response_assignment = response.context['latest_assignment']

        self.assertIsInstance(response_assignment, CourseAssignment)
        self.assertFalse(response_assignment.is_attending)
        self.assertIsInstance(
            response.context['form'], ExistingUserApplicationForm)
        self.assertEqual(
            HASNT_ATTENDED_LAST_ENROLLED_COURSE_ERROR, response.context['header_text'])
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('apply.html', response)

        users_count_before = User.objects.count()
        applications_count_before = Application.objects.count()
        apply_response = self.client.post(reverse(
            'applications:apply'), {'course': course.pk, 'skype': 'foobar', 'phone': '007'})
        applications_count_after = Application.objects.count()
        users_count_after = User.objects.count()

        self.assertEqual(302, apply_response.status_code)
        self.assertTemplateUsed('thanks.html', apply_response)
        self.assertEqual(
            applications_count_before + 1, applications_count_after)
        self.assertEqual(users_count_before, users_count_after)

    def test_apply_when_user_who_attended_last_course_he_applied_for(self):
        course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
        )
        expired_course = Course.objects.create(
            name='Expired Course',
            url='expired-course',
            application_until=datetime(1900, 1, 1),
        )
        CourseAssignment.objects.create(course=expired_course, user=self.user,
                                        group_time=1)
        self.client.login(username='user@user.com', password='123')
        response = self.client.get(reverse('applications:apply'))
        response_assignment = response.context['latest_assignment']

        self.assertIsInstance(response_assignment, CourseAssignment)
        self.assertTrue(response_assignment.is_attending)
        self.assertIsInstance(
            response.context['form'], ExistingAttendingUserApplicationForm)
        self.assertEqual(
            HAS_ATTENDED_LAST_ENROLLED_COURSE_MESSAGE, response.context['header_text'])
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('apply.html', response)

        users_count_before = User.objects.count()
        applications_count_before = Application.objects.count()
        assignments_count_before = CourseAssignment.objects.count()
        apply_response = self.client.post(
            reverse('applications:apply'), {'course': course.pk, 'group_time': 1})
        applications_count_after = Application.objects.count()
        users_count_after = User.objects.count()
        assignments_count_after = CourseAssignment.objects.count()

        self.assertEqual(302, apply_response.status_code)
        self.assertTemplateUsed('thanks.html', apply_response)
        self.assertEqual(applications_count_before, applications_count_after)
        self.assertEqual(users_count_before, users_count_after)
        self.assertEqual(assignments_count_before + 1, assignments_count_after)

    def test_thanks(self):
        response = self.client.get(reverse('applications:thanks'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('thanks.html', response)


class ApplicationSolutionViewsTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
        )

        self.student_user = User.objects.create_user(
            'ivo_student@gmail.com', '123')
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
        self.third_wheel = User.objects.create_user(
            'third_wheel@gmail.com', '456')

        self.green_task = ApplicationTask.objects.create(
            name='Green task',
            course=self.course,
        )
        self.task_url = 'https://github.com/HackBulgaria/Frontend-JavaScript-1/tree/master/week1/2-jQuery-Gauntlet'
        self.task = ApplicationTask.objects.create(
            course=self.course, description=self.task_url, name='<2> jQuery-Gauntlet')
        self.solution_url = 'https://github.com/syndbg/HackBulgaria/'
        self.solution = ApplicationSolution.objects.create(
            task=self.task, student=self.student_user, repo=self.solution_url)

    def test_add_solution_allows_only_POST(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('applications:add_solution'))
        self.assertEqual(405, response.status_code)

    def test_add_solution_not_existing_task(self):
        before_adding = ApplicationSolution.objects.count()
        self.client.login(username='ivo_student@gmail.com', password='123')

        response = self.client.post(reverse('applications:add_solution'),
                                    {
            'task': 3777,
            'repo': 'https://github.com/HackBulgaria/Odin',
        })
        after_adding = ApplicationSolution.objects.count()
        self.assertEqual(before_adding, after_adding)
        self.assertEqual(422, response.status_code)

    def test_add_solution(self):
        self.client.login(username='ivo_student@gmail.com', password='123')

        before_adding = ApplicationSolution.objects.count()
        response = self.client.post(reverse('applications:add_solution'),
                                    {
            'task': self.green_task.pk,
            'repo': 'https://github.com/HackBulgaria/Odin',
        })
        after_adding = ApplicationSolution.objects.count()

        self.assertEqual(before_adding + 1, after_adding)
        self.assertEqual(200, response.status_code)

    # TODO: Write isolated tests first starting from students.forms where
    # The form is based from.
    def test_edit_solution(self):
        self.client.login(username='ivo_student@gmail.com', password='123')

        before_adding = ApplicationSolution.objects.count()
        response = self.client.post(reverse('applications:add_solution'),
                                    {
            'task': self.green_task.pk,
            'repo': 'https://github.com/HackBulgaria/OdinG',
        })

        self.assertEqual(200, response.status_code)
        self.assertEqual(before_adding + 1, ApplicationSolution.objects.count())

        solution = ApplicationSolution.objects.get(task=self.green_task)
        self.assertEqual('https://github.com/HackBulgaria/OdinG', solution.repo)

        response = self.client.post(reverse('applications:add_solution'),
                                    {
            'task': self.green_task.pk,
            'repo': 'https://github.com/HackBulgaria/Odin2',
        })

        solution = ApplicationSolution.objects.get(task=self.green_task)
        self.assertEqual('https://github.com/HackBulgaria/Odin2', solution.repo)

        after_adding = ApplicationSolution.objects.count()

        self.assertEqual(before_adding + 1, after_adding)
        self.assertEqual(200, response.status_code)

    def test_submit_solutions_not_for_anonymous_users(self):
        response = self.client.get(
            reverse('applications:solutions', kwargs={'course_url': self.course.url}))
        self.assertRedirects(
            response, '/login/?next=/applications/{0}/solutions'.format(self.course.url))

    def test_submit_solutions(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(
            reverse('applications:solutions', kwargs={'course_url': self.course.url}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('admission_solutions.html', response)
