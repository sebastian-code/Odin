from django.core.urlresolvers import reverse
from django.test import TestCase

from faq.models import Faq


class FaqViewsTest(TestCase):
    def setUp(self):
        self.faq = Faq.objects.create(title='Lorem ipsum', text='Lorem ipsum dolor sit amet,\
        consectetur adipiscing elit.')

    def test_show_faqs(self):
        response = self.client.get(reverse('faq:show_faqs'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_faqs.html', response)
