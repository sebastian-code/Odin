import os

from django.core.management import call_command
from django.test import TestCase

from .models import User


class GetCommandsTest(TestCase):
    def setUp(self):
        self.filename = 'students.txt'
        self.user_without_github = User.objects.create_user('asd@gmail.com', '123')
        self.user_without_github.first_name = 'Asd'
        self.user_without_github.save()

        self.user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.user.first_name = 'Ivo'
        self.user.status = User.STUDENT
        self.user.github_account = 'https://github.com/Ivaylo-Bachvarov'
        self.user.save()

    def tearDown(self):
        os.remove(self.filename)

    def test_get_people_with_no_github(self):
        expected = '[1] {} - {}\n'.format(self.user_without_github.first_name, self.user_without_github.email)
        call_command('get_people_with_no_github', self.filename)
        with open(self.filename, 'r') as f:
            actual = f.read()
        self.assertEqual(expected, actual)

    def test_get_github_accounts(self):
        expected = '{} - {} - {}\n'.format(self.user.first_name, self.user.email, self.user.github_account)
        call_command('get_github_accounts', self.filename)
        with open(self.filename, 'r') as f:
            actual = f.read()
        self.assertEqual(expected, actual)
