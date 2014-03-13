from django.shortcuts import redirect, render
from django.contrib.auth import views


def login(request):
    if request.user.is_authenticated():
        return redirect('/profile')
    else:
        return views.login(request, template_name='login_form.html')


def user_profile(request):
    return render(request, "profile.html", locals())
