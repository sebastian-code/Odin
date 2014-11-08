import datetime

from django.test import TestCase

from courses.models import Course, Task
from students.management.commands.generate_certificates import is_new_valid_github_account
from students.management.commands.helpers.classes import TempCertificate, GithubSolution
from students.models import User, CourseAssignment, Solution


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
        expected_datetime = datetime.datetime.combine(self.start_time, datetime.datetime.min.time())
        self.assertEqual(expected_datetime, self.temp_certificate.start_time)

    def test_set_end_time(self):
        raw_date = self.end_time + datetime.timedelta(days=31)
        expected_datetime = datetime.datetime.combine(raw_date, datetime.datetime.min.time())
        self.assertEqual(expected_datetime, self.temp_certificate.end_time)

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
