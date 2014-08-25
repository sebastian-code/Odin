from django.test import TestCase


class WebsiteTest(TestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('index.html', response)
