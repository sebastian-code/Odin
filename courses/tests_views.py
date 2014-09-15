import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Course, Task, Certificate
from students.models import User, CourseAssignment, Solution


class CoursesViewsTest(TestCase):

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
        response = self.client.get(
            reverse('courses:show_course', kwargs={'course_url': self.course.url}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_course.html', response)

    def test_show_nonexistent_course(self):
        response = self.client.get(
            reverse('courses:show_course', kwargs={'course_url': 'some_url'}))
        self.assertEqual(404, response.status_code)
        self.assertTemplateNotUsed('show_course.html', response)

    def test_show_all_courses_when_no_active_courses(self):
        response = self.client.get(reverse('courses:show_all_courses'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_all_courses.html', response)
        self.assertNotContains(response, 'id="active_courses"')
        self.assertContains(response, 'id="no_active_courses"')

    def test_show_all_courses_when_active_courses(self):
        self.course.start_time = datetime.date.today()
        self.course.save()
        response = self.client.get(reverse('courses:show_all_courses'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_all_courses.html', response)
        self.assertContains(response, 'id="active_courses"')
        self.assertNotContains(response, 'id="no_active_courses"')

    def test_show_all_courses_when_no_upcoming_courses(self):
        self.course.delete()
        response = self.client.get(reverse('courses:show_all_courses'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_all_courses.html', response)
        self.assertNotContains(response, 'id="upcoming_courses"')
        self.assertContains(response, 'id="no_upcoming_courses"')

    def test_show_all_courses_when_upcoming_courses(self):
        self.course.start_time = None
        self.course.save()
        response = self.client.get(reverse('courses:show_all_courses'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_all_courses.html', response)
        self.assertContains(response, 'id="upcoming_courses"')
        self.assertNotContains(response, 'id="no_upcoming_courses"')

    def test_show_all_courses_when_no_ended_courses(self):
        response = self.client.get(reverse('courses:show_all_courses'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_all_courses.html', response)
        self.assertNotContains(response, 'id="ended_courses"')
        self.assertContains(response, 'id="no_ended_courses"')

    def test_show_all_courses_when_ended_courses(self):
        self.course.start_time = datetime.date.today() - datetime.timedelta(days=30)
        self.course.end_time = datetime.date.today() - datetime.timedelta(days=1)
        self.course.save()
        response = self.client.get(reverse('courses:show_all_courses'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_all_courses.html', response)
        self.assertContains(response, 'id="ended_courses"')
        self.assertNotContains(response, 'id="no_ended_courses"')

    def test_show_all_partners(self):
        response = self.client.get(reverse('courses:show_all_partners'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_all_partners.html', response)

    def test_show_course_students(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(
            reverse('courses:show_course_students', kwargs={'course_id': self.course.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_course_students.html', response)


class CertificateViewsTest(TestCase):

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
            name='task1',
            course=self.course,
        )

        self.task2 = Task.objects.create(
            name='task2',
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

    def test_show_certificate(self):
        response = self.client.get(self.certificate.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_certificate.html', response)

    def test_certificate_show_solution(self):
        response = self.client.get(self.certificate.get_absolute_url())
        self.assertContains(response, 'class="code-sent"')

    def test_certificate_show_not_sended_solution_alert(self):
        response = self.client.get(self.certificate.get_absolute_url())
        self.assertContains(response, 'class="code-not-sent"')
