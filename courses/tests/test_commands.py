import datetime

from django.test import TestCase
from django.utils import timezone

from github import Repository
import mock

from courses.management.commands import generate_tasks
from courses.models import Course, Task


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
        expected = timezone.now().replace(hour=23, minute=56, second=56)
        expected = expected + datetime.timedelta(days=7)
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

    def test_get_formatted_dir_name(self):
        raw_dir_week = 'week5'
        raw_dir_exam = 'exam2'

        expected_dir_week = 'Week 5'
        expected_dir_exam = 'Exam 2'
        self.assertEqual(expected_dir_week, generate_tasks.get_formatted_dir_name(raw_dir_week))
        self.assertEqual(expected_dir_exam, generate_tasks.get_formatted_dir_name(raw_dir_exam))

    def test_create_db_task(self):
        course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
            git_repository='https://github.com/HackBulgaria/Frontend-JavaScript-1/'
        )
        tree_element = mock.MagicMock()
        task_github_url = 'https://github.com/HackBulgaria/Frontend-JavaScript-1/tree/master/week1/2-jQuery-Gauntlet/'
        tree_element.path = 'week1/2-jQuery-Gauntlet/README.md'
        expected = 'Created task <2> jQuery Gauntlet - https://github.com/HackBulgaria/Frontend-JavaScript-1/tree/master/week1/2-jQuery-Gauntlet/'
        self.assertEqual(expected, generate_tasks.create_db_task(course, tree_element, False))
        self.assertIsNotNone(Task.DoesNotExist, Task.objects.get(description=task_github_url))
