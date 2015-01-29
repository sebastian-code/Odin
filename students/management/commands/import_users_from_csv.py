import csv
import time

from django.core.management.base import BaseCommand
from django.conf import settings

from students.models import User, CourseAssignment
from courses.models import Course


class Command(BaseCommand):
    args = '<path_to_csv_file>'
    help = '''
        I will import users from the csv file.
        I will generate random passwords and send emails to them.
        You can edit the email template located in students/management/commands/template.txt
        The format of the CSV file must be:
            email, first_name last_name, 1/2, course_id, works_at, is_online
        * 1 is for early group_time
        * 2 is for late group_time

        * 1 is_online True
        * 0 is_online False

        !!IMPORTANT: your emails and names must not contain comma [,].
        We use the comma for value separation!

        May the force be with you!
    '''

    def handle(self, *args, **options):
        TEMPLATE_PATH = '/students/management/commands/helpers/template.txt'

        with open(args[0], 'r') as csvfile:
            csv_line = csv.reader(csvfile, delimiter=',', quotechar='|')

            with open(settings.BASE_DIR + TEMPLATE_PATH) as template_file:
                template_text = template_file.read()

                for row in csv_line:
                    email = row[0]
                    full_name = row[1].strip().split(' ')
                    group_time = row[2].strip()
                    course_id = row[3].strip()
                    works_at = row[4].strip()
                    is_online = row[5].strip()
                    new_password = 'You know your password!'

                    current_course = Course.objects.get(id=course_id)
                    if not current_course:
                        raise Exception('Invalid course given for' + email)

                    elif not User.is_existing(email):
                        first_name = full_name[0]
                        last_name = full_name[-1]
                        new_password = User.objects.make_random_password()
                        User.objects.create_user(
                            email,
                            new_password,
                            first_name,
                            last_name,
                            works_at
                        )

                    new_user = User.objects.get(email=email)

                    if not CourseAssignment.is_existing(new_user, current_course):
                        CourseAssignment.objects.create(user=new_user, course=current_course, group_time=group_time, is_online=is_online)

                    email_text = template_text.format(full_name[0], email, new_password)
                    new_user.email_user('Registration in hackbulgaria.com', email_text)
                    full_name = ' '.join(full_name)
                    print(full_name + ' registered successfully')
                    time.sleep(2)
