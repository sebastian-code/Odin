import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from courses.models import Course, Partner
from students.models import User


class StatisticsViewsTest(TestCase):

    def setUp(self):
        self.staff_user = User.objects.create_user('staff@staff.com', '123')
        self.staff_user.is_staff = True
        self.staff_user.save()
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
        )

        self.partner = Partner.objects.create(name='Potato Company', description='Potato company')

    def test_dashboard(self):
        self.client.login(username='staff@staff.com', password='123')
        response = self.client.get(reverse('statistics:dashboard'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('dashboard.html', response)

    def test_show_partners_stats(self):
        self.client.login(username='staff@staff.com', password='123')
        response = self.client.get(reverse('statistics:show_partners_stats'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_partners_stats.html', response)

    def test_show_partner_stats(self):
        self.client.login(username='staff@staff.com', password='123')
        response = self.client.get(reverse('statistics:show_partner_stats', kwargs={'partner_id': self.partner.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_partner_company_stats.html', response)

    def test_show_companies_stats(self):
        self.client.login(username='staff@staff.com', password='123')
        response = self.client.get(reverse('statistics:show_companies_stats'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_partner_company_stats.html', response)

    def test_show_all_assignments_stats(self):
        response = self.client.get(reverse('statistics:show_all_assignments_stats'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_assignment_stats.html', response)

    def test_show_active_assignments_stats(self):
        response = self.client.get(reverse('statistics:show_active_assignments_stats'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_assignment_stats.html', response)

    def test_show_expired_assignments_stats(self):
        response = self.client.get(reverse('statistics:show_expired_assignments_stats'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_assignment_stats.html', response)

    def test_show_courses_stats(self):
        self.client.login(username='staff@staff.com', password='123')
        response = self.client.get(reverse('statistics:show_courses_stats'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_courses_stats.html', response)

    def test_show_course_stats(self):
        self.client.login(username='staff@staff.com', password='123')
        response = self.client.get(reverse('statistics:show_course_stats', kwargs={'course_id': self.course.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_course_stats.html', response)
