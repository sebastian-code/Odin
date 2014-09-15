from django.test import TestCase, client
from django.core.urlresolvers import reverse

from .models import Faq


class FaqModelTest(TestCase):
    def setUp(self):
        self.faq = Faq.objects.create(title='Lorem ipsum', text='Lorem ipsum dolor sit amet,\
        consectetur adipiscing elit.')

    def test_unicode(self):
        self.assertEqual(self.faq.title, unicode(self.faq))
