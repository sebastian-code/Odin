import sys

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'odintest',
        'USER':     'travis',
        'PASSWORD': '',
        'HOST':     'localhost',
        'PORT':     '',
    }
}

SOUTH_TESTS_MIGRATE = False  # To disable migrations and use syncdb instead
SKIP_SOUTH_TESTS = True  # To disable South's own unit tests
USE_DEBUG_TOOLBAR = False

GITHUB_OATH_TOKEN = ''
DOMAIN = 'hackbulgaria.com'
CHECKIN_TOKEN = '123'
