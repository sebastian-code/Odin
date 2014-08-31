from django.conf import settings
from courses.models import WeeklyCommit, Certificate

from github import Github, GithubException
from datetime import date, timedelta


class TempCertificate:

    def __init__(self, assignment):
        self.assignment = assignment
        self.weekly_commits = []
        self.open_issues = 0
        self.closed_issues = 0
        self.total_commits = 0
        self.has_cheated = True
        self.cheated_solutions = []
        self.start_time = self.__set_start_time()
        self.end_time = self.__set_end_time()

    def __set_start_time(self):
        start_time = self.assignment.course.start_time
        return date(year=start_time.year, month=start_time.month, day=start_time.day)

    def __set_end_time(self):
        end_time = self.assignment.course.end_time + timedelta(days=31)
        return date(year=end_time.year, month=end_time.month, day=end_time.day)

    def get_total_commits(self):
        return reduce(lambda x, y: x + y, map(lambda x: x.commits_count, self.weekly_commits), 0)

    def update_stats(self, api_stats_dictionary):
        self.open_issues += api_stats_dictionary['open_issues']
        self.closed_issues += api_stats_dictionary['closed_issues']

    def add_cheated_solution(self, solution):
        self.cheated_solutions.append(solution)
        self.has_cheated = True

    def save_weekly_commit_in_db(self, solution_github_repo):
        commits_count = solution_github_repo.get_commits_count()
        weekly_commit = WeeklyCommit.objects.create(commits_count=commits_count)
        self.weekly_commits.append(weekly_commit)

    def log_cheating(self):
        course_name = self.cheated_solutions[0].task.course
        user = self.cheated_solutions[0].user
        filename = 'Cheater[{}] {} - {}'.format(course_name, user, user.email)
        with open(filename, 'w+') as f:
            for i, solution in enumerate(self.cheated_solutions, start=1):
                f.write('{}) Cheated on task {} - {}. Given solution - {}\n'.format(i, solution.task.name, solution.task.description, solution.repo))

    def save_certificate_in_db(self):
        db_certificate = Certificate.objects.create(assignment=self.assignment, issues_closed=self.closed_issues, issues_opened=self.open_issues, total_commits=self.get_total_commits())
        # can't reference a list as a ManyToManyField argument
        for w in self.weekly_commits:
            db_certificate.weekly_commits.add(w)

    def log_or_save_in_db(self):
        if self.has_cheated and self.cheated_solutions:
            self.log_cheating()
        else:
            Certificate.objects.filter(assignment=self.assignment).delete()
            self.save_certificate_in_db()
            print 'Created certificate for {}'.format(self.assignment.user)


class GithubSolution:

    def __init__(self, user_name, repo_name, solution):
        self.solution = solution
        self.api_repo = self.__set_api_repo(user_name, repo_name)
        self.commits_count = 0

    def __set_api_repo(self, user_name, repo_name):
        github_client = Github(settings.GITHUB_OATH_TOKEN)
        try:
            return github_client.get_user(user_name).get_repo(repo_name)
        except GithubException:
            return None

    def is_invalid_repo(self):
        return self.api_repo is None

    def is_cheating(self):
        profile_github_account = self.solution.get_user_github_username()
        return self.api_repo.has_in_collaborators(profile_github_account) is False

    def is_fork(self):
        return self.api_repo.fork

    def update_commits_count(self, start, end):
        author = self.solution.get_user_github_username()
        commits = self.api_repo.get_commits(since=start, until=end, author=author)
        count = self.__count_commits(commits)
        count = count if count > 0 else self.__count_commits(self.api_repo.get_commits(since=start, until=end))
        self.commits_count = count

    def get_commits_count(self):
        return self.commits_count

    def __count_commits(self, commits):
        count = 0
        for c in commits:
            count += 1
        return count

    # no API functionality for that
    def get_closed_issues_count(self):
        count = 0
        try:
            for issue in self.api_repo.get_issues(state='closed'):
                if issue.closed_at:  # GithubObject.NotSet
                    count += 1
        # if opening/closing issues is disabled
        except GithubException:
            count = 0
        return count

    def get_stats(self):
        return {'open_issues': self.api_repo.open_issues_count, 'closed_issues': self.get_closed_issues_count()}
