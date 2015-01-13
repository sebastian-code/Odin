from django.shortcuts import render, redirect

from .forms import ApplicationForm


def apply(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('applications:thanks')

    else:
        form = ApplicationForm()

    return render(request, 'apply.html', locals())


def thanks(request):
    return render(request, 'thanks.html', locals())
