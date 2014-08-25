from django.test import TestCase, client
from django.core.urlresolvers import reverse

from .models import Faq


class FaqTest(TestCase):
    def setUp(self):
        self.faq = Faq.objects.create(title='Lorem ipsum', text='Lorem ipsum dolor sit amet,\
        consectetur adipiscing elit.')

    def test_unicode(self):
        self.assertEqual(self.faq.title, unicode(self.faq))

    def test_show_faqs(self):
        self.client = client.Client()
        response = self.client.get(reverse('faq:show-faqs'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('show_faqs.html', response)
