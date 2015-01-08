from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from students.models import User

from .forms import ApplicationForm
from .helper import register_user
from .models import Application


def apply(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            new_user = register_user(form.cleaned_data)
            wanted_course = form.cleaned_data['course']

            application = Application(
                student=new_user,
                course=wanted_course
            )
            application.save()

            return redirect('applications:thanks')

    else:
        form = ApplicationForm()

    return render(request, 'apply.html', locals())


def thanks(request):
    return render(request, 'thanks.html', locals())
