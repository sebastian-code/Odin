DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '', # Or path to database file if using sqlite3
        # Remove the following if using sqlite3
        'USER': '',
        'PASSWORD': '',
        'HOST': '', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Empty for default
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
