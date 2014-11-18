from django.shortcuts import render

from courses.models import Course


def index(request):
    courses = Course.objects.filter(show_on_index=True)
    return render(request, 'index.html', locals())


def page_not_found(request):
    return render(request, '404.html')


def server_error(request):
    return render(request, '500.html')
