from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from students.models import CourseAssignment


class Command(BaseCommand):
    args = '<filename>'
    help = '''
        Lists in <filename>.txt, all students without a github account.
    '''

    def handle(self, *args, **options):
        filename = args[0]
        file_write = open(filename, 'w+')
        assignments = CourseAssignment.objects.exclude(Q(user__github_account__contains='https://github.com/') | Q(user__github_account__contains='http://github.com'))
        for i, obj in enumerate(assignments, start=1):
            student = obj.user
            file_write.write('[{}] {} - {}'.format(i, student.get_full_name().encode('utf-8'), student.email) + '\n')
        file_write.close()
