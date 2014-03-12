from django.shortcuts import render
from courses.models import Course


def index(request):
    courses = Course.objects.filter(show_on_index=True)

    return render(request, "index.html", locals())
