from django.core.management.base import BaseCommand
from django.db.models import Q
from students.models import User


class Command(BaseCommand):
    args = '<filename>'
    help = '''
        Lists in <filename>.txt, all students without a github account.
    '''

    def handle(self, *args, **options):
        filename = args[0]
        file_write = open(filename, 'w+')
        no_git_students = User.objects.exclude(Q(github_account__contains='//github.com/'))
        
        for i, student in enumerate(no_git_students, start=1):
            file_write.write('[{}] {} - {}'.format(i, student.get_full_name().encode('utf-8'), student.email) + '\n')

        file_write.close()
