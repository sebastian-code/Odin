from django.conf import settings
from github import Github, GithubException


class TempCertificate:

    def __init__(self):
        self.weekly_commits = []
        self.open_issues = 0
        self.closed_issues = 0
        self.total_commits = 0

    def get_total_commits(self):
        return reduce(lambda x, y: x + y, map(lambda x: x.commits_count, self.weekly_commits))

    def update_stats(self, api_stats_dictionary):
        self.open_issues += api_stats_dictionary['open_issues']
        self.closed_issues += api_stats_dictionary['closed_issues']


class SolutionGithubRepo:

    def __init__(self, user, repo_name):
        self.api_repo = self.__set_api_repo(user, repo_name)

    def __set_api_repo(self, user, repo_name):
        github_client = Github(settings.GITHUB_OATH_TOKEN)
        return github_client.get_user(user).get_repo(repo_name)

    def get_commits_count(self, start, end):
        commits = self.api_repo.get_commits(since=start, until=end)
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
