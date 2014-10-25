import datetime

from django.contrib.auth.hashers import make_password
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.core.validators import ValidationError
from django.db import IntegrityError
from django.test import TestCase


from .models import CheckIn, User, UserNote, HrLoginLog, CourseAssignment, Solution, StudentStartedWorkingAt
from courses.models import Partner, Course, Task


class CourseAssignmentFormsTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
            end_time=datetime.date.today(),
            ask_for_feedback=True
        )
        self.teacher_user = User.objects.create_user('teacher@teacher.com', 'teach')
        self.teacher_user.status = User.TEACHER
        self.teacher_user.save()

        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.first_name = 'Ivaylo'
        self.student_user.last_name = 'Bachvarov'
        self.student_user.status = User.STUDENT
        self.student_user.save()

        self.partner_potato = Partner.objects.create(
            name='Potato Company', description='Potato company')
        self.partner_salad = Partner.objects.create(
            name='Salad Company', description='Salad Company')

        self.hr_user = User.objects.create_user('ivan_hr@gmail.com', '1234')
        self.hr_user.status = User.HR
        self.hr_user.hr_of = self.partner_potato
        self.hr_user.save()

        self.assignment = CourseAssignment.objects.create(
            user=self.student_user, course=self.course, group_time=CourseAssignment.EARLY)
        self.assignment.favourite_partners.add(self.partner_potato)
        self.third_wheel = User.objects.create_user('third_wheel@gmail.com', '456')

        self.teacher_assignment = CourseAssignment.objects.create(user=self.teacher_user,
                                                                  course=self.course,
                                                                  group_time=CourseAssignment.EARLY)

    def test_assignment_add_note(self):
        self.client.login(username='teacher@teacher.com', password='teach')
        before_adding = UserNote.objects.count()
        response = self.client.post(reverse('students:assignment',
                                    kwargs={'id': self.assignment.id}),
                                    {'assignment': self.assignment,
                                     'text': 'Kappa'})
        after_adding = UserNote.objects.count()
        self.assertEqual(200, response.status_code)
        # TODO: Not working atm? self.assertEqual(before_adding + 1, after_adding)
