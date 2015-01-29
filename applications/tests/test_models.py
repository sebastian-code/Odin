from django.core import mail
from django.test import TestCase
from django.utils import timezone

from applications.models import Application
from courses.models import Course
from students.models import CourseAssignment, User


class ApplicationModelTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
        )
        self.student = User.objects.create(
            email='foo@bar.com'
        )
        self.application = Application.objects.create(
            course=self.course,
            student=self.student,
        )

    def test_string_representation(self):
        expected = 'Application for course <{0}> by <{1}>'.format(self.course, self.student)
        self.assertEqual(expected, str(self.application))

    def test_get_assignment_when_not_existing(self):
        self.assertIsNone(self.application.get_assignment())

    def test_get_assigment_when_existing(self):
        assignment = CourseAssignment.objects.create(
            course=self.course,
            user=self.student,
            group_time=1,
        )
        actual_assignment = self.application.get_assignment()
        self.assertEqual(assignment.pk, actual_assignment.pk)
        self.assertEqual(assignment.pk, actual_assignment.pk)

    def test_get_assignment_url_when_not_existing(self):
        self.assertIsNone(self.application.get_assignment_url())

    def test_get_assignment_url_when_existing(self):
        assignment = CourseAssignment.objects.create(
            course=self.course,
            user=self.student,
            group_time=1,
            )
        expected_url = assignment.get_absolute_url()
        self.assertEqual(expected_url, self.application.get_assignment_url())

    def test_email_student(self):
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            subject = 'test_email_student'
            message = 'testing'

            self.application.email_student(subject, message)
            sent_mail = mail.outbox[0]

            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(subject, sent_mail.subject)
            self.assertEqual(message, sent_mail.body)
