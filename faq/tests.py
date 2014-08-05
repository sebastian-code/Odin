from django.test import TestCase, client
from django.core.urlresolvers import reverse


class FaqTest(TestCase):

    def test_faq_list_view(self):
        self.client = client.Client()
        response = self.client.get(reverse('faq:show-faqs'))
        self.assertEqual(200, response.status_code)
