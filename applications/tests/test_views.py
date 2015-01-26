from django.utils import timezone
from django.core.urlresolvers import reverse
from django.test import TestCase

from applications.models import Application, ApplicationSolution, ApplicationTask
from courses.models import Course, Partner
from students.models import CourseAssignment, User


class ApplicationViewsTest(TestCase):

    def setUp(self):
        pass

    def test_thanks(self):
        response = self.client.get(reverse('applications:thanks'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('thanks.html', response)


class SolutionViewsTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=timezone.now(),
        )

        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.github_account = 'https://github.com/Ivaylo-Bachvarov'
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

        self.green_task = ApplicationTask.objects.create(
            name='Green task',
            course=self.course,
        )
        self.task_url = 'https://github.com/HackBulgaria/Frontend-JavaScript-1/tree/master/week1/2-jQuery-Gauntlet'
        self.task = ApplicationTask.objects.create(course=self.course, description=self.task_url, name='<2> jQuery-Gauntlet')
        self.solution_url = 'https://github.com/syndbg/HackBulgaria/'
        self.solution = ApplicationSolution.objects.create(task=self.task, student=self.student_user, repo=self.solution_url)

    def test_add_solution_get_status(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('applications:add_solution'))
        self.assertEqual(405, response.status_code)

    def test_add_solution_not_existing_task(self):
        before_adding = ApplicationSolution.objects.count()
        self.client.login(username='ivo_student@gmail.com', password='123')

        response = self.client.post(reverse('applications:add_solution'),
                                    {
            'task': 3777,
            'repo': 'https://github.com/HackBulgaria/Odin',
        })
        after_adding = ApplicationSolution.objects.count()
        self.assertEqual(before_adding, after_adding)
        self.assertEqual(422, response.status_code)

    def test_add_solution_status_code(self):
        self.client.login(username='ivo_student@gmail.com', password='123')

        before_adding = ApplicationSolution.objects.count()
        response = self.client.post(reverse('applications:add_solution'),
                                    {
            'task': self.green_task.id,
            'repo': 'https://github.com/HackBulgaria/Odin',
        })
        after_adding = ApplicationSolution.objects.count()

        self.assertEqual(before_adding + 1, after_adding)
        self.assertEqual(200, response.status_code)

    def test_edit_solution(self):
        self.client.login(username='ivo_student@gmail.com', password='123')

        before_adding = ApplicationSolution.objects.count()
        response = self.client.post(reverse('applications:add_solution'),
                                    {
            'task': self.green_task.id,
            'repo': 'https://github.com/HackBulgaria/Odin',
        })

        response = self.client.post(reverse('applications:add_solution'),
                                    {
            'task': self.green_task.id,
            'repo': 'https://github.com/HackBulgaria/Odin2',
        })

        after_adding = ApplicationSolution.objects.count()

        self.assertEqual(before_adding + 1, after_adding)
        self.assertEqual(200, response.status_code)

    def test_view_solutions(self):
        self.client.login(username='ivo_student@gmail.com', password='123')
        response = self.client.get(reverse('applications:solutions', kwargs={'course_url': self.course.url}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('solutions.html', response)
