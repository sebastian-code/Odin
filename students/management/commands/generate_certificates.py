from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from students.models import CourseAssignment, Solution
from courses.models import WeeklyCommit, Certificate

from datetime import datetime
from github import Github


# WILL BE MOVED TO ITS OWN COMMAND SOON!
# def get_people_with_no_github(course_students, filename):
#     file_students_without_github_account = open(filename, 'w+')
#     for obj in course_students:
#         student = obj.user
#         github_account = student.github_account
#         if github_account is None or not 'github' in github_account:
# it's great when the DB isn't even UTF-8...
#             file_students_without_github_account.write(
#                 student.get_full_name().encode('utf-8') + '\n')
#     file_students_without_github_account.close()


def generate_certificate(assignment, solutions):
    is_cheater = False
    visited_repos = []
    weekly_commits = []
    closed_issues = 0
    open_issues = 0

    for solution in solutions:
        if solution:
            github_parameters = get_user_and_repo_names(solution.repo)
            # The form validation logic will be moved away from here soon!
            if len(github_parameters) == 2 and not github_parameters in visited_repos:
                user_github = get_user_and_repo_names(solution.user.github_account)[0]
                repo = get_repo(github_parameters)
                if github_parameters[0] != user_github and not repo.has_in_collaborators(user_github):
                    is_cheater = True
                    break
                stats = generate_stats(repo)
                visited_repos.append(github_parameters)
                open_issues += stats['open_issues']
                closed_issues += stats['closed_issues']

                # do we need a start field in the model?
                model_startime = solution.task.course.application_until
                start_time = datetime(
                    year=model_startime.year, month=model_startime.month, day=model_startime.day)

                model_endtime = solution.task.deadline
                end_time = datetime(
                    year=model_endtime.year, month=model_endtime.month, day=model_endtime.day)

                commits_count = get_commits_count(repo, start_time, end_time)
                weekly_commit = WeeklyCommit.objects.create(commits_count=commits_count)
                weekly_commits.append(weekly_commit)

    if is_cheater:
        return
    if len(weekly_commits) > 0:
        total_commits = reduce(
            lambda x, y: x + y, list(map(lambda x: x.commits_count, weekly_commits)))
        certificate = Certificate.objects.create(
            assignment=assignment, issues_closed=closed_issues, issues_opened=open_issues, total_commits=total_commits)
        # can't reference a list as a ManyToManyField argument
        for w in weekly_commits:
            certificate.weekly_commits.add(w)


def get_commits_count(repo, start, end):
    commits = repo.get_commits(since=start, until=end)
    count = 0
    for c in commits:
        count += 1
    return count


def get_repo(github_parameters):
    github_client = Github(settings.GITHUB_OATH_TOKEN)
    return github_client.get_user(github_parameters[0]).get_repo(github_parameters[1])


def generate_stats(repo):
    closed_issues = get_closed_issues_count(repo)
    stats = {'open_issues': repo.open_issues_count, 'closed_issues': closed_issues}
    print stats
    return stats


# no API functionality for that
def get_closed_issues_count(repo):
    count = 0
    for issue in repo.get_issues(state='closed'):
        if not issue.closed_at is None:  # GithubObject.NotSet
            count += 1
    return count


def get_user_and_repo_names(github_url):
    # Ex: https://github.com/syndbg/HackBulgaria/tree/master/Core-Java-1
    # Becomes  [u'https:', u'', u'github.com', u'syndbg', u'HackBulgaria', u'tree', u'master', u'Core-Java-1']
    # Only 4th and 5th elements are relevant
    github_url_split = github_url.split('/')[3:]
    return [github_url_split[0], github_url_split[1]] if len(github_url_split) >= 2 else [github_url_split[0]]


class Command(BaseCommand):
    args = '<course_name>'
    help = '''
        Generates certificates for every student from <course_name>.
    '''

    def handle(self, *args, **options):
        assignments = CourseAssignment.objects.filter(course__name=args[0])
        for assignment in assignments:
            solutions = Solution.objects.filter(user=assignment.user, task__course__name=args[0])
            github_account = assignment.user.github_account
            # useless to generate certificate for someone who doesn't have a github account?
            if github_account and 'https://github.com/' in github_account and len(solutions) > 0:
                generate_certificate(assignment, solutions)
