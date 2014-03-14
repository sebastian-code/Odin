from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import views
from .forms import UserEditForm


def login(request):
    if request.user.is_authenticated():
        return redirect('profile')
    else:
        return views.login(request, template_name='login_form.html')


def logout(request):
    views.logout(request)
    return redirect('/')


def user_profile(request):
    return render(request, "profile.html", locals())


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile/')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'edit_profile.html', locals())
