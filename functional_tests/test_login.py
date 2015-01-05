#!/usr/bin/env python
# coding=utf-8
from .base import FunctionalTest

from django.contrib.auth import get_user_model


User = get_user_model()


class LoginTest(FunctionalTest):

    def test_login_with_hr(self):
        User.objects.create(email='hr@hackbulgara.com', password='sony', status=User.HR)
        # Open the site
        self.browser.get(self.server_ur)
        # Click the login button and get redirected to /login
        self.browser.find_element_by_id('login').click()
        self.assertIn('Вход', self.browser.title, 'Not redirected to login')
        # Enter username, password and press login.
        username_field = self.browser.find_element_by_name('username')
        password_field = self.browser.find_element_by_name('password')
        username_field.send_keys('hr@hackbulgaria.com')
        password_field.send_keys('sony')
        self.browser.find_element_by_tag_name('button').click()
        # Should see the HR panel
        profile_button = self.browser.find_element_by_id('profile')
        logout_button = self.browser.find_element_by_id('logout')
        self.assertIsNotNone(logout_button, 'Not logged in!')
        self.assertEqual('HR панел', profile_button)
