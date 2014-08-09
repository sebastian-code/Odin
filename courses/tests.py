from django.core.urlresolvers import reverse
from django.test import TestCase, client

from students.models import User, CourseAssignment, Solution
from .models import Course, Task, Certificate

import datetime


class CoursesTest(TestCase):

    def setUp(self):
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.save()

        self.hr_user = User.objects.create_user('ivo_hr@gmail.com', '123')
        self.hr_user.status = User.HR
        self.hr_user.save()

        self.teacher_user = User.objects.create_user('ivo_teacher@gmail.com', '123')
        self.teacher_user.status = User.TEACHER
        self.teacher_user.save()

        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
        )

    def test_show_course(self):
        self.client = client.Client()
        response = self.client.get(
            reverse('courses:show-course',  kwargs={'course_url': self.course.url}))
        self.assertEqual(200, response.status_code)

    def test_show_nonexistent_course(self):
        self.client = client.Client()
        response = self.client.get(
            reverse('courses:show-course',  kwargs={'course_url': 'some_url'}))
        self.assertEqual(404, response.status_code)

    def test_show_course_students(self):
        self.client = client.Client()
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(
            reverse('courses:course-students',  kwargs={'course_id': self.course.id}))
        self.assertEqual(200, response.status_code)


class CertificateTest(TestCase):
    def setUp(self):
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.save()

        self.course = Course.objects.create(
            name='JavaScript',
            url='JavaScript',
            application_until=datetime.datetime.now(),
        )

        self.assignment = CourseAssignment.objects.create(
            user=self.student_user, 
            course=self.course, 
            group_time=CourseAssignment.EARLY
        )

        self.task1 = Task.objects.create(
            name="task1",
            course=self.course,
        )

        self.task2 = Task.objects.create(
            name="task2",
            course=self.course,
        )

        self.solution1 = Solution.objects.create(
            task=self.task1,
            user=self.student_user
        )

        self.certificate = Certificate.objects.create(
            assignment=self.assignment,
            issues_closed=5,
            issues_opened=10,
            total_commits=15
        )


    def test_certificate_status_code(self):
        self.client = client.Client()
        response = self.client.get(
            reverse('courses:show-certificate',  kwargs={'certificate_id': self.certificate.id}))
        self.assertEqual(200, response.status_code)

    #TODO: More tests when the template is done!
