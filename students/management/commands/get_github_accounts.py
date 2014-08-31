from django.core.management.base import BaseCommand

from students.models import User


class Command(BaseCommand):
    args = '<filename>'
    help = '''
        Lists in <filename>, all students github accounts.
    '''

    def handle(self, *args, **options):
        filename = args[0]
        output = User.objects.filter(github_account__contains='://github.com/')
        with open(filename, 'w+') as f:
            for usr in output:
                f.write('{} - {} - {}\n'.format(usr, usr.email, usr.github_account))
