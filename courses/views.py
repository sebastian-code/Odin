from django.shortcuts import render, get_object_or_404
from .models import Course
from datetime import datetime


def show_course(request, course_url):
    course = get_object_or_404(Course, url=course_url)
    enable_applications = datetime.today().date() <= course.application_until
    return render(request, "show_course.html", locals())


def show_all_courses(request):
    courses = Course.objects.all()

    return render(request, "show_all_courses.html", locals())
