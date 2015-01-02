import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver

from .server_tools import reset_database


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                domain = arg.split('=')[1]
                cls.server_host = domain
                cls.server_url = 'http://' + domain
                cls.against_staging = True
                return
        super().setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if not cls.against_staging:
            super().tearDownClass()

    def setUp(self):
        if self.against_staging:
            reset_database(self.server_host)
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
