DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
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

# Ask the system for token and place it here1
CHECKIN_TOKEN = 'TOKEN FROM CHECKIN SYSTEM HERE'