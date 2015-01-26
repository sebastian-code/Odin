from django.core.urlresolvers import reverse
from django.test import TestCase


class ApplicationViewsTest(TestCase):

    def setUp(self):
        pass

    def test_thanks(self):
        response = self.client.get(reverse('applications:thanks'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('thanks.html', response)
