import datetime

from django.test import TestCase

from .models import Course, Certificate, Partner, Task
from students.models import CourseAssignment, User


class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
        )

    def test_unicode(self):
        self.assertEqual('Test Course', unicode(self.course))

    def test_get_statistics_url(self):
        expected = '/stats/courses/{}/'.format(self.course.id)
        self.assertEqual(expected, self.course.get_statistics_url())


class PartnerModelTest(TestCase):
    def setUp(self):
        self.partner = Partner.objects.create(name='Potato Company', description='Potato company')

    def test_unicode(self):
        self.assertEqual(self.partner.name, unicode(self.partner))

    def test_get_statistics_url(self):
        expected = '/stats/partners/{}/'.format(self.partner.id)
        self.assertEqual(expected, self.partner.get_statistics_url())


class TaskModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
        )
        self.task = Task.objects.create(
            name='task1',
            course=self.course,
        )

    def test_unicode(self):
        self.assertEqual('task1', unicode(self.task))


class CertificateModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
        )
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.save()
        self.assignment = CourseAssignment.objects.create(
            user=self.student_user,
            course=self.course,
            group_time=CourseAssignment.EARLY
        )
        self.certificate = Certificate.objects.create(
            assignment=self.assignment,
            issues_closed=5,
            issues_opened=10,
            total_commits=15
        )

    def test_get_absolute_url(self):
        expected = '/certificate/{}/'.format(self.assignment.id)
        self.assertEqual(expected, self.certificate.get_absolute_url())
