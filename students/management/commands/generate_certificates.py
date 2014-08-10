from django.core.management.base import BaseCommand


from students.models import CourseAssignment, Solution
from .helpers.classes import TempCertificate, SolutionGithubRepo
from courses.models import WeeklyCommit, Certificate
from datetime import datetime


def generate_certificate(assignment, solutions):
    visited_repos = []
    temp_certificate = TempCertificate()
    is_cheater = False
    cheated_solutions = []

    for solution in solutions:
        github_parameters = solution.get_github_user_and_repo_names()
        if is_new_valid_github_account(github_parameters, visited_repos):
            solution_github_repo = SolutionGithubRepo(github_parameters['user'], github_parameters['repo_name'])
            if is_cheating(github_parameters, solution, solution_github_repo):
                cheated_solutions.append(solution)
                is_cheater = True
                continue
            api_stats = solution_github_repo.get_stats()
            temp_certificate.update_stats(api_stats)
            create_db_weekly_commit(solution, solution_github_repo, temp_certificate.weekly_commits)
            visited_repos.append(github_parameters)

    if is_cheater:
        log_cheating(cheated_solutions)
    else:
        Certificate.objects.filter(assignment=assignment).delete()
        print 'Created certificate'
        create_db_certificate(assignment, temp_certificate)


def is_new_valid_github_account(github_parameters, visited_repos):
    return 'user' in github_parameters and 'repo_name' in github_parameters and not github_parameters in visited_repos


def is_cheating(github_parameters, solution, solution_github_repo):
    profile_github_account = solution.get_user_github_username()
    return github_parameters['user'] != profile_github_account and solution_github_repo.api_repo.has_in_collaborators(profile_github_account) == False


def log_cheating(cheated_solutions):
    task = cheated_solutions[0].task
    user = cheated_solutions[0].user
    filename = 'Cheater[{}] {} - {}'.format(task.course, user.get_full_name(), user.email)
    f = open(filename, 'w+')
    for i, solution in enumerate(cheated_solutions, start=1):
        f.write('{}) Cheated on task {} - {}. Given solution - {}'.format(i, task.name, task.description, solution.repo) + '\n')
    f.close()


def create_db_certificate(assignment, certificate_object):
    db_certificate = Certificate.objects.create(
        assignment=assignment, issues_closed=certificate_object.closed_issues, issues_opened=certificate_object.open_issues, total_commits=certificate_object.get_total_commits())
    # can't reference a list as a ManyToManyField argument
    for w in certificate_object.weekly_commits:
        db_certificate.weekly_commits.add(w)


def create_db_weekly_commit(solution, solution_github_repo, weekly_commits):
    model_startime = solution.task.course.application_until
    start_time = datetime(year=model_startime.year, month=model_startime.month, day=model_startime.day)

    model_endtime = solution.task.deadline
    end_time = datetime(year=model_endtime.year, month=model_endtime.month, day=model_endtime.day)

    commits_count = solution_github_repo.get_commits_count(start_time, end_time)
    weekly_commit = WeeklyCommit.objects.create(commits_count=commits_count)
    weekly_commits.append(weekly_commit)


class Command(BaseCommand):
    args = '<course_id>'
    help = '''
        Generates certificates for every student from <course_id>.
    '''

    def handle(self, *args, **options):
        arg_course_id = args[0]
        assignments = CourseAssignment.objects.filter(course__id=arg_course_id)
        for assignment in assignments:
            solutions = Solution.objects.filter(user=assignment.user, task__course__id=arg_course_id)

            if assignment.has_valid_github_account() and solutions:
                generate_certificate(assignment, solutions)
