# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*18ji*lhdl*-z7smqprw8g1r!ez0&n78s1kjue#g3@s(^hx%z('


DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',  # Or path to database file if using sqlite3
        # Remove the following if using sqlite3
        'USER': '',
        'PASSWORD': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'HOST': '',
        'PORT': '',  # Empty for default
    }
}

ALLOWED_HOSTS = []

DEBUG = True

TEMPLATE_DEBUG = True

EMAIL_HOST = ''
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = ''

CORS_ORIGIN_ALLOW_ALL = False
DOMAIN = 'hackbulgaria.com'
# Ask the system for token and place it here
CHECKIN_TOKEN = 'TOKEN FROM CHECKIN SYSTEM HERE'
# https://help.github.com/articles/creating-an-access-token-for-command-line-use
GITHUB_OATH_TOKEN = ''