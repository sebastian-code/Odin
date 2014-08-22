import datetime
import mock
from github import Repository

from django.core.urlresolvers import reverse
from django.test import TestCase, client
from django.utils import timezone

from .management.commands import generate_tasks
from students.models import User, CourseAssignment, Solution
from .models import Course, Task, Certificate, Partner


class CoursesTest(TestCase):

    def setUp(self):
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.save()

        self.hr_user = User.objects.create_user('ivo_hr@gmail.com', '123')
        self.hr_user.status = User.HR
        self.hr_user.save()

        self.teacher_user = User.objects.create_user('ivo_teacher@gmail.com', '123')
        self.teacher_user.status = User.TEACHER
        self.teacher_user.save()

        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
        )

    def test_show_course(self):
        self.client = client.Client()
        response = self.client.get(
            reverse('courses:show-course', kwargs={'course_url': self.course.url}))
        self.assertEqual(200, response.status_code)

    def test_show_nonexistent_course(self):
        self.client = client.Client()
        response = self.client.get(
            reverse('courses:show-course', kwargs={'course_url': 'some_url'}))
        self.assertEqual(404, response.status_code)

    def test_show_course_students(self):
        self.client = client.Client()
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(
            reverse('courses:course-students', kwargs={'course_id': self.course.id}))
        self.assertEqual(200, response.status_code)


class PartnerTest(TestCase):
    def setUp(self):
        self.partner = Partner.objects.create(name='Potato Company', description='Potato company')

    def test_unicode(self):
        self.assertEqual(self.partner.name, unicode(self.partner))


class CertificateTest(TestCase):

    def setUp(self):
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.save()

        self.course = Course.objects.create(
            name='JavaScript',
            url='JavaScript',
            application_until=datetime.datetime.now(),
        )

        self.assignment = CourseAssignment.objects.create(
            user=self.student_user,
            course=self.course,
            group_time=CourseAssignment.EARLY
        )

        self.task1 = Task.objects.create(
            name="task1",
            course=self.course,
        )

        self.task2 = Task.objects.create(
            name="task2",
            course=self.course,
        )

        self.solution1 = Solution.objects.create(
            task=self.task1,
            user=self.student_user
        )

        self.certificate = Certificate.objects.create(
            assignment=self.assignment,
            issues_closed=5,
            issues_opened=10,
            total_commits=15
        )

    def test_certificate_status_code(self):
        self.client = client.Client()
        response = self.client.get(self.certificate.get_absolute_url())
        self.assertEqual(200, response.status_code)

    def test_certificate_show_solution(self):
        self.client = client.Client()
        response = self.client.get(self.certificate.get_absolute_url())
        self.assertContains(response, 'class="code-sent"')

    def test_certificate_show_not_sended_solution_alert(self):
        self.client = client.Client()
        response = self.client.get(self.certificate.get_absolute_url())
        self.assertContains(response, 'class="code-not-sent"')


class TaskGenerationTest(TestCase):
    @mock.patch('courses.management.commands.generate_tasks.Github')
    def test_get_api_repo(self, mocked_github):
        github_parameters = {'user': 'syndbg', 'repo_name': 'HackBulgaria'}
        mocked_github.get_user.get_repo.return_value = Repository
        generate_tasks.get_api_repo(github_parameters)
        self.assertTrue(mocked_github.called)

    def test_get_user_and_repo_names(self):
        url = 'https://github.com/syndbg/HackBulgaria/tree/master/Core-Java-1'
        result = generate_tasks.get_user_and_repo_names(url)
        self.assertEqual('syndbg', result['user'])
        self.assertEqual('HackBulgaria', result['repo_name'])
        url = 'https://github.com/syndbg/'
        result = generate_tasks.get_user_and_repo_names(url)
        self.assertEqual('syndbg', result['user'])
        self.assertEqual('', result['repo_name'])

    def test_is_weekly_task(self):
        mocked = mock.MagicMock()
        mocked.path = 'week1/2-jQuery-Gauntlet/README.md'
        self.assertTrue(generate_tasks.is_weekly_task(mocked))
        mocked.path = 'week1/2-jQuery-Gauntlet/10/README.md'
        self.assertFalse(generate_tasks.is_weekly_task(mocked))

    def test_is_exam_task(self):
        mocked = mock.MagicMock()
        mocked.path = 'exams/exam1/1-Beers-And-Fries/README.md'
        self.assertTrue(generate_tasks.is_exam_task(mocked))
        mocked.path = 'exams/exam2/README.md'
        self.assertFalse(generate_tasks.is_exam_task(mocked))

    def test_get_dir_and_task_names(self):
        path = 'exams/exam1/1-Beers-And-Fries/README.md'
        result = generate_tasks.get_dir_and_task_names(path)
        self.assertEqual('/1-Beers-And-Fries/', result['raw_task'])
        self.assertEqual('exam1', result['dir'])

        path = 'week6/3-Multiuser-Paint/README.md'
        result = generate_tasks.get_dir_and_task_names(path)
        self.assertEqual('/3-Multiuser-Paint/', result['raw_task'])
        self.assertEqual('week6', result['dir'])

    def test_get_deadline(self):
        expected = timezone.now()
        expected = expected.replace(day=expected.day + 7, hour=23, minute=56, second=56)
        result = generate_tasks.get_deadline()
        self.assertEqual(expected.day, result.day)
        self.assertEqual(expected.hour, result.hour)
        self.assertEqual(expected.minute, result.minute)
        self.assertEqual(expected.second, result.second)

    def test_get_formatted_task_url(self):
        raw_task_url = 'https://github.com/HackBulgaria/Frontend-JavaScript-1'
        dir_task_names = {'raw_task': '/2-File-Upload-With-Progress/', 'dir': 'week8'}
        expected = 'https://github.com/HackBulgaria/Frontend-JavaScript-1/tree/master/week8/2-File-Upload-With-Progress/'
        self.assertEqual(expected, generate_tasks.get_formatted_task_url(raw_task_url, dir_task_names, False))

        dir_task_names = {'raw_task': '/2-Timer-Of-Destiny/', 'dir': 'exam1'}
        expected = 'https://github.com/HackBulgaria/Frontend-JavaScript-1/tree/master/exams/exam1/2-Timer-Of-Destiny/'
        self.assertEqual(expected, generate_tasks.get_formatted_task_url(raw_task_url, dir_task_names, True))

    def test_get_formatted_task_name(self):
        raw_task_name = '/1-A-Set-of-Functional-Problems/'
        expected = '<1> A Set of Functional Problems'
        self.assertEqual(expected, generate_tasks.get_formatted_task_name(raw_task_name))

    def test_create_db_task(self):
        course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
            git_repository='https://github.com/HackBulgaria/Frontend-JavaScript-1/'
        )
        tree_element = mock.MagicMock()
        tree_element.path = 'week1/2-jQuery-Gauntlet/README.md'
        task_github_url = 'https://github.com/HackBulgaria/Frontend-JavaScript-1/tree/master/week1/2-jQuery-Gauntlet/'
        generate_tasks.create_db_task(course, tree_element, False)
        self.assertIsNotNone(Task.DoesNotExist, Task.objects.get(description=task_github_url))
