from django.shortcuts import render

from courses.models import Course


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]


def index(request):
    current_user = request.user
    if current_user.is_authenticated():
        is_student = current_user.status == current_user.STUDENT
        is_hr = current_user.status == current_user.HR
        is_teacher = current_user.status == current_user.TEACHER
    courses = Course.objects.filter(show_on_index=True).order_by('-id')

    courses_chunked = list(chunks(courses, 2))

    return render(request, 'index.html', locals())


def page_not_found(request):
    return render(request, '404.html')


def server_error(request):
    return render(request, '500.html')
