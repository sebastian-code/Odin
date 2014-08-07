import sys

# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*18ji*lhdl*-z7smqprw8g1r!ez0&n78s1kjue#g3@s(^hx%z('

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
