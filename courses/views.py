from django.shortcuts import render, get_object_or_404
from .models import Course


def show_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(request, "show_course.html", locals())
