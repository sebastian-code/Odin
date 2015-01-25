import re

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_mac(mac):
    # RegexValidator uses re.search, which has no use for us
    regex = re.compile(r'^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$', re.IGNORECASE)
    if not re.match(regex, mac):
        raise ValidationError('{} is not a valid mac address'.format(mac), 'invalid_mac_address')


def validate_url(url, needle, message, code):
    www_needle = '://www.{}'.format(needle)
    needle = '://{}'.format(needle)

    URLValidator(url)
    if needle not in url and www_needle not in url:
        raise ValidationError(message, code)


def validate_github(url):
    validate_url(url, 'github.com', '{} is not a valid Github account URL'.format(url), 'invalid_github_account_url')


def validate_linkedin(url):
    validate_url(url, 'linkedin.com', '{} is not a valid Linkedin account URL'.format(url), 'invalid_linkedin_account_url')
