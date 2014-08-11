from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from students.models import CourseAssignment, User, Solution
from .models import Course, Partner, Certificate, Task


def show_course(request, course_url):
    course = get_object_or_404(Course, url=course_url)
    enable_applications = datetime.today().date() <= course.application_until
    return render(request, "show_course.html", locals())


def show_all_courses(request):
    courses = Course.objects.all()

    return render(request, "show_all_courses.html", locals())


def show_all_partners(request):
    partners = Partner.objects.all()

    return render(request, "show_all_partners.html", locals())


def course_materials(request):

    return render(request, "show_materials.html", locals())


@login_required
def course_students(request, course_id):
    assignments = CourseAssignment.objects.filter(course=course_id, user__status=User.STUDENT)
    is_teacher_or_hr = request.user.status == User.HR or request.user.status == User.TEACHER
    if request.user.hr_of:
        interested_in_me = CourseAssignment.objects.filter(
            course=course_id,
            favourite_partners=request.user.hr_of,
            user__status=User.STUDENT
        )
    return render(request, "course_students.html", locals())


def show_certificate(request, assignment_id):
    certificate = get_object_or_404(Certificate, assignment=assignment_id)
    user = certificate.assignment.user
    course = certificate.assignment.course
    tasks = Task.objects.filter(course=course)
    solutions = Solution.objects.filter(task__in=tasks, user=user)

    # Zips solutions with tasks
    solutions_by_task = {}
    for solution in solutions:
        solutions_by_task[solution.task.id] = solution

    for task in tasks:
        if task.id in solutions_by_task:
            task.solution = solutions_by_task[task.id]

    return render(request, "show_certificate.html", locals())
