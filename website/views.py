from django.shortcuts import render

from courses.models import Course


def index(request):
    current_user = request.user
    if current_user.is_authenticated():
        is_student = current_user.status == current_user.STUDENT
        is_hr = current_user.status == current_user.HR
        is_teacher = current_user.status == current_user.TEACHER
    courses = Course.objects.filter(show_on_index=True)
    return render(request, 'index.html', locals())


def page_not_found(request):
    return render(request, '404.html')


def server_error(request):
    return render(request, '500.html')
