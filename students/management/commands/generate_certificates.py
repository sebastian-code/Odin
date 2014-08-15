from django.core.management.base import BaseCommand


from students.models import CourseAssignment, Solution
from .helpers.classes import TempCertificate, SolutionGithubRepo


def generate_certificate(assignment, solutions):
    visited_repos = []
    temp_certificate = TempCertificate(assignment)

    for solution in solutions:
        github_parameters = solution.get_github_user_and_repo_names()

        if is_new_valid_github_account(github_parameters, visited_repos):
            solution_github_repo = SolutionGithubRepo(github_parameters['user'], github_parameters['repo_name'], solution)
            if solution_github_repo.is_invalid_repo():
                return
            if solution_github_repo.is_cheating():
                temp_certificate.add_cheated_solution(solution)
                continue
            api_stats = solution_github_repo.get_stats()
            temp_certificate.update_stats(api_stats)
            temp_certificate.save_weekly_commit_in_db(solution, solution_github_repo)
            visited_repos.append(github_parameters)
    temp_certificate.log_or_save_in_db()


def is_new_valid_github_account(github_parameters, visited_repos):
    if 'user' in github_parameters and 'repo_name' in github_parameters:
        for param in visited_repos:
            if param['user'] == github_parameters['user'] and param['repo_name'] == github_parameters['repo_name']:
                return False
    return True


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
