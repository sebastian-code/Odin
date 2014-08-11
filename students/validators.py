from django.core.exceptions import ValidationError

import re


# Model field validators
def validate_mac(mac):
    # RegexValidator uses re.search, which has no use for us
    regex = re.compile(r'^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$', re.IGNORECASE)
    if not re.match(regex, mac):
        raise ValidationError('{} is not a valid mac address'.format(mac), 'invalid_mac_address')


# Form validators
