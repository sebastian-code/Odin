from django.utils import unittest
from django.test.client import Client
from .models import CheckIn, User

client = Client()

class CheckInCase(unittest.TestCase):
    def setUp(self):
        self.new_user = User.objects.create_user('ivan@abv.bg', '123')
        self.new_user.mac = '4c:80:93:1f:a4:50'
        self.new_user.save()

    def tearDown(self):
        self.new_user.delete()

    def test_new_check_in_status(self):
        response = client.post('/set-check-in/', {'mac': self.new_user.mac})
        self.assertEqual(response.status_code, 200)

    def test_new_check_in_result(self):
        response = client.post('/set-check-in/', {'mac': self.new_user.mac})
        checkin = CheckIn.objects.get(student=self.new_user)

        assert checkin is not None

    def test_new_check_in_case_insensitive(self):
        response = client.post('/set-check-in/', {'mac': self.new_user.mac.upper()})
        checkin = CheckIn.objects.get(student=self.new_user)

        assert checkin is not None