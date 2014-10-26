import unittest

from django.core.validators import ValidationError

from students.validators import validate_mac, validate_url, validate_github, validate_linkedin


class ValidatorsTest(unittest.TestCase):

    def test_validate_mac(self):
        invalid_mac = ':ez:77:b4:14:66:b'
        self.assertRaises(ValidationError, validate_mac, invalid_mac)
        valid_mac = 'bd:88:d0:19:63:c9'
        self.assertIsNone(validate_mac(valid_mac))

    def test_validate_url_when_invalid_url(self):
        invalid_url = '%invalid%[/]*url.com'
        self.assertRaises(ValidationError, validate_url, invalid_url, 'github', 'invalid url given', 'invalid_url')

    def test_validate_www_url(self):
        valid_url = 'http://www.hackbulgaria.com'
        self.assertIsNone(validate_url(valid_url, 'hackbulgaria.com', 'invalid url given', 'invalid_url'))

    def test_valdiate_url(self):
        valid_url = 'http://hackbulgaria.com'
        self.assertIsNone(validate_url(valid_url, 'hackbulgaria.com', 'invalid url given', 'invalid_url'))

    def test_validate_github(self):
        valid_url = 'https://github.com/HackBulgaria/Odin'
        www_valid_url = 'https://www.github.com/HackBulgaria/Odin'

        self.assertIsNone(validate_github(valid_url))
        self.assertIsNone(validate_github(www_valid_url))

    def test_validate_linkedin(self):
        valid_url = 'https://linkedin.com/in/jeffweiner08gst'  # Linkedin CEO
        www_valid_url = 'https://www.linkedin.com/in/jeffweiner08gst'

        self.assertIsNone(validate_linkedin(valid_url))
        self.assertIsNone(validate_linkedin(www_valid_url))
