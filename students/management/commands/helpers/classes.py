from django.conf import settings
from courses.models import WeeklyCommit, Certificate

from github import Github, GithubException
from datetime import datetime


class TempCertificate:

    def __init__(self, assignment):
        self.assignment = assignment
        self.weekly_commits = []
        self.open_issues = 0
        self.closed_issues = 0
        self.total_commits = 0
        self.has_cheated = True
        self.cheated_solutions = []

    def get_total_commits(self):
        return reduce(lambda x, y: x + y, map(lambda x: x.commits_count, self.weekly_commits))

    def update_stats(self, api_stats_dictionary):
        self.open_issues += api_stats_dictionary['open_issues']
        self.closed_issues += api_stats_dictionary['closed_issues']

    def add_cheated_solution(self, db_solution):
        self.cheated_solutions.append(db_solution)
        self.has_cheated = True

    def create_db_weekly_commit(self, db_solution, solution_github_repo):
        model_startime = db_solution.task.course.application_until
        start_time = datetime(year=model_startime.year, month=model_startime.month, day=model_startime.day)

        model_endtime = db_solution.task.deadline
        end_time = datetime(year=model_endtime.year, month=model_endtime.month, day=model_endtime.day)

        commits_count = solution_github_repo.get_commits_count(start_time, end_time)
        weekly_commit = WeeklyCommit.objects.create(commits_count=commits_count)
        self.weekly_commits.append(weekly_commit)

    def log_cheating(self):
        course_name = self.cheated_solutions[0].task.course
        user = self.cheated_solutions[0].user
        filename = 'Cheater[{}] {} - {}'.format(course_name, user, user.email)
        f = open(filename, 'w+')
        for i, solution in enumerate(self.cheated_solutions, start=1):
            f.write('{}) Cheated on task {} - {}. Given solution - {}\n'.format(i, solution.task.name, solution.task.description, solution.repo))
        f.close()

    def create_db_certificate(self):
        db_certificate = Certificate.objects.create(assignment=self.assignment, issues_closed=self.closed_issues, issues_opened=self.open_issues, total_commits=self.get_total_commits())
        # can't reference a list as a ManyToManyField argument
        for w in self.weekly_commits:
            db_certificate.weekly_commits.add(w)

    def log_or_add_in_db(self):
        if self.has_cheated and self.cheated_solutions:
            self.log_cheating()
        else:
            print self.weekly_commits
            Certificate.objects.filter(assignment=self.assignment).delete()
            self.create_db_certificate()
            print 'Created certificate for {}'.format(self.assignment.user)


class SolutionGithubRepo:

    def __init__(self, user, repo_name, db_solution):
        self.db_solution = db_solution
        self.api_repo = self.__set_api_repo(user, repo_name)

    def __set_api_repo(self, user, repo_name):
        github_client = Github(settings.GITHUB_OATH_TOKEN)
        return github_client.get_user(user).get_repo(repo_name)

    def is_cheating(self):
        profile_github_account = self.db_solution.get_user_github_username()
        return self.api_repo.has_in_collaborators(profile_github_account) is False

    def get_commits_count(self, start, end):
        author = self.db_solution.get_user_github_username()
        print author
        commits = self.api_repo.get_commits(since=start, until=end, author=author)
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
