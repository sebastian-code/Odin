from django.core.management.base import BaseCommand, CommandError
from students.models import User, CourseAssignment
from courses.models import Course
from django.conf import settings

import csv
import string
import random
import time

def random_password(size=9, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


class Command(BaseCommand):
    args = '<path_to_csv_file>'
    help = '''
        I will import users from the csv file. 
        I will generate a random passwords for them and send some emails to them.
        You can edit the email template is is located in students/management/commands/tempalte.txt
        The format of the CSV file must be like: email, fisrt_name last_name, 1/2, course_id, works_at
        1 is for early group_time
        2 is for late group_time
        
        !!IMPORTANT: your emails and names must not contain comma [,] we use the comma for value separation!

        May the force be with you!
    '''

    def handle(self, *args, **options):
        with open(args[0], 'r') as csvfile:
            csv_line = csv.reader(csvfile, delimiter=',', quotechar='|')

            template = open(settings.BASE_DIR + '/students/management/commands/template.txt')
            template_text = template.read()
            template.close()
            
            for row in csv_line:
                email = row[0]
                full_name = row[1].strip().split(" ")
                new_password = random_password()
                group_time = row[2].strip()
                course_id = row[3].strip()
                works_at = row[4].strip()

                current_course = Course.objects.filter(id=course_id).first()
                if not current_course:  
                    raise Exception("Invalid course given for" + email)

                new_user = User.objects.create_user(email, new_password)
                new_user.first_name = full_name[0]
                new_user.last_name = full_name[-1]
                new_user.works_at = works_at
                new_user.save()

                assignment = CourseAssignment(user=new_user, course=current_course, group_time=group_time)
                assignment.save()
                
                email_text = template_text.format(full_name[0], email, new_password)
                new_user.email_user("Registration in hackbulgaria.com", email_text)
                print(" ".join(full_name) + " registered successfully")
                time.sleep(2)     
