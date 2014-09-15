import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from courses.models import Course, Partner


class StatisticsViewsTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            url='test-course',
            application_until=datetime.datetime.now(),
        )

        self.partner = Partner.objects.create(name='Potato Company', description='Potato company')

    # TODO: implement the view
    def test_dashboard(self):
        pass

    def test_show_partners_stats(self):
        response = self.client.get(reverse('statistics:show_partners_stats'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_partners_stats.html', response)

    def test_show_partner_stats(self):
        response = self.client.get(reverse('statistics:show_partner_stats', kwargs={'partner_id': 1}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_partner_company_stats.html', response)

    def test_show_non_existent_partner_stats(self):
        response = self.client.get(reverse('statistics:show_partner_stats', kwargs={'partner_id': 55}))
        self.assertEqual(404, response.status_code)
        self.assertTemplateNotUsed('show_partner_company_stats.html', response)

    def test_show_companies_stats(self):
        response = self.client.get(reverse('statistics:show_companies_stats'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_partner_company_stats.html', response)

    # TODO: implement the view
    def test_show_assignments_stats(self):
        pass

    def test_show_courses_stats(self):
        pass

    def test_show_course_stats(self):
        response = self.client.get(reverse('statistics:show_course_stats', kwargs={'course_id': self.course.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_course_stats.html', response)

    def test_show_non_existent_course_stats(self):
        response = self.client.get(reverse('statistics:show_course_stats', kwargs={'course_id': 100}))
        self.assertEqual(404, response.status_code)
        self.assertTemplateNotUsed('show_course_stats.html', response)
