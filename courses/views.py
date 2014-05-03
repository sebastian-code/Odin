from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course
from students.models import CourseAssignment
from datetime import datetime


def show_course(request, course_url):
    course = get_object_or_404(Course, url=course_url)
    enable_applications = datetime.today().date() <= course.application_until
    return render(request, "show_course.html", locals())


def show_all_courses(request):
    courses = Course.objects.all()

    return render(request, "show_all_courses.html", locals())


def course_materials(request):

    return render(request, "show_materials.html", locals())


@login_required
def course_students(request, course_id):
    assignments = CourseAssignment.objects.filter(course=course_id)

    return render(request, "course_students.html", locals())
