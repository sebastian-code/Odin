"""
Django settings for odin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition

INSTALLED_APPS = (
    # must be initialized before admin
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'adminfiles',
    'adminsortable',
    'debug_toolbar',
    'markdown_deux',
    'pagedown',
    'tinymce',

    'courses',
    'faq',
    'forum',
    'polls',
    'statistics',
    'students',
    'website',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'odin.urls'

WSGI_APPLICATION = 'odin.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'students.User'
LOGIN_URL = 'students:login'
NO_AVATAR_IMG = 'img/no-avatar.png'

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

DJANGO_WYSIWYG_FLAVOR = "tinymce_advanced"

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'width': 900,
    'height': 400,
}

AWESOME_AVATAR = {
    'width': 150,
    'height': 150,

    'save_quality': 90,
    'save_format': 'png',
}

try:
    if 'TRAVIS' in os.environ:
        from travis_settings import *
    else:
        from local_settings import *

except ImportError:
    exit("{}_settings.py not found!".format("travis" if 'TRAVIS' in os.environ else "local"))
