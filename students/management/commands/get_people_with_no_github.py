from django.core.management.base import BaseCommand

from students.models import User


class Command(BaseCommand):
    args = '<filename>'
    help = '''
        Lists in <filename>, all students without a github account.
    '''

    def handle(self, *args, **options):
        filename = args[0]
        # status = 1 (STUDENT)
        students = User.objects.filter(status=1).exclude(github_account__contains='//github.com')
        with open(filename, 'w+') as f:
            for i, student in enumerate(students, start=1):
                f.write('[{}] {} - {}\n'.format(i, student.get_full_name(),
                                 student.email))
