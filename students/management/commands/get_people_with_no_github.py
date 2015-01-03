from django.core.management.base import BaseCommand

from students.models import User


class Command(BaseCommand):
    args = '<filename>'
    help = '''
        Lists in <filename>, all students without a github account.
    '''

    def handle(self, *args, **options):
        filename = args[0]
        students = User.objects.filter(status=User.STUDENT).exclude(github_account__contains='//github.com')
        with open(filename, 'w+') as f:
            for i, student in enumerate(students, start=User.STUDENT):
                f.write('[{}] {} - {}\n'.format(i, student.get_full_name(), student.email))
