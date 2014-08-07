from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from students.models import CourseAssignment, Solution
from courses.models import WeeklyCommit, Certificate

from datetime import datetime
from github import Github


class TempCertificate:

    def __init__(self):
        self.weekly_commits = []
        self.closed_issues = 0
        self.open_issues = 0
        self.total_commits = 0

    def get_total_commits(self):
        total_commits = reduce(
            lambda x, y: x + y, map(lambda x: x.commits_count, self.weekly_commits))
        return total_commits


def generate_certificate(assignment, solutions):
    visited_repos = []
    temp_certificate = TempCertificate()
    is_cheater = False
    cheated_solutions = []

    for solution in solutions:
        github_parameters = get_user_and_repo_names(solution.repo)
        if is_valid_github_account(github_parameters, visited_repos):
            api_repo_object = get_api_repo(github_parameters)
            if is_cheating(github_parameters, api_repo_object, solution):
                cheated_solutions.append(solution)
                is_cheater = True
                continue
            api_stats = generate_api_stats(api_repo_object)
            update_stats(temp_certificate, api_stats)
            create_weekly_commit_object(solution, api_repo_object, temp_certificate.weekly_commits)
            visited_repos.append(github_parameters)

    if is_cheater:
        log_cheating(cheated_solutions)
    elif temp_certificate.weekly_commits:
        create_db_certificate(assignment, temp_certificate)


def is_valid_github_account(github_parameters, visited_repos):
    return len(github_parameters) == 2 and not github_parameters in visited_repos


def is_cheating(github_parameters, api_repo_object, solution):
    profile_github_account = get_user_and_repo_names(solution.user.github_account)['user']
    return github_parameters['user'] != profile_github_account and api_repo_object.has_in_collaborators(profile_github_account) == False


def update_stats(temp_certificate, api_stats):
    temp_certificate.open_issues += api_stats['open_issues']
    temp_certificate.closed_issues += api_stats['closed_issues']


def log_cheating(cheated_solutions):
    task = cheated_solutions[0].task
    user = cheated_solutions[0].user
    filename = 'Cheater[{}] {} - {}'.format(task.course, user.get_full_name(), user.email)
    f = open(filename, 'w+')
    for i, solution in enumerate(cheated_solutions, start=1):
        f.write('{}) Cheated on task {} - {}. Given solution - {}'.format(i,
                                                                          task.name, task.description, solution.repo) + '\n')
    f.close()


def create_db_certificate(assignment, certificate_object):
    db_certificate = Certificate.objects.create(
        assignment=assignment, issues_closed=certificate_object.closed_issues, issues_opened=certificate_object.open_issues, total_commits=certificate_object.get_total_commits())
    # can't reference a list as a ManyToManyField argument
    for w in certificate_object.weekly_commits:
        db_certificate.weekly_commits.add(w)


def create_weekly_commit_object(solution, api_repo_object, weekly_commits):
    model_startime = solution.task.course.application_until
    start_time = datetime(
        year=model_startime.year, month=model_startime.month, day=model_startime.day)

    model_endtime = solution.task.deadline
    end_time = datetime(year=model_endtime.year, month=model_endtime.month, day=model_endtime.day)

    commits_count = get_commits_count(api_repo_object, start_time, end_time)
    weekly_commit = WeeklyCommit.objects.create(commits_count=commits_count)
    weekly_commits.append(weekly_commit)


def get_commits_count(repo, start, end):
    commits = repo.get_commits(since=start, until=end)
    count = 0
    for c in commits:
        count += 1
    return count


def get_api_repo(github_parameters):
    github_client = Github(settings.GITHUB_OATH_TOKEN)
    return github_client.get_user(github_parameters['user']).get_repo(github_parameters['repo_name'])


def generate_api_stats(repo):
    closed_issues = get_closed_issues_count(repo)
    stats = {'open_issues': repo.open_issues_count, 'closed_issues': closed_issues}
    print stats
    return stats


# no API functionality for that
def get_closed_issues_count(repo):
    count = 0
    for issue in repo.get_issues(state='closed'):
        if issue.closed_at:  # GithubObject.NotSet
            count += 1
    return count


def get_user_and_repo_names(github_url):
    # Ex: https://github.com/syndbg/HackBulgaria/tree/master/Core-Java-1
    # Becomes  [u'https:', u'', u'github.com', u'syndbg', u'HackBulgaria', u'tree', u'master', u'Core-Java-1']
    # Only 4th and 5th elements are relevant
    github_url_split = github_url.split('/')[3:]
    return {'user': github_url_split[0], 'repo_name': github_url_split[1]} if len(github_url_split) >= 2 else {'user': github_url_split[0]}


def is_valid_assignment(assignment, solutions):
    github_account = assignment.user.github_account
    return github_account is not None and '://github.com/' in github_account and len(solutions) > 0


class Command(BaseCommand):
    args = '<course_id>'
    help = '''
        Generates certificates for every student from <course_id>.
    '''

    def handle(self, *args, **options):
        arg_course_id = args[0]
        assignments = CourseAssignment.objects.filter(course__id=arg_course_id)
        for assignment in assignments:
            solutions = Solution.objects.filter(
                user=assignment.user, task__course__id=arg_course_id)

            if is_valid_assignment(assignment, solutions):
                generate_certificate(assignment, solutions)
