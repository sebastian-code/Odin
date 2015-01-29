from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


LOGIN_URL = settings.LOGIN_URL


def teacher_required(function, login_url=LOGIN_URL):
    decorator = user_passes_test(lambda u: u.is_teacher() or u.is_staff)
    if function:
        return decorator(function)
    return decorator
