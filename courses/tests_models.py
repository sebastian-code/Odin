from django.test import TestCase

from .models import Partner


class PartnerTest(TestCase):
    def setUp(self):
        self.partner = Partner.objects.create(name='Potato Company', description='Potato company')

    def test_unicode(self):
        self.assertEqual(self.partner.name, unicode(self.partner))
