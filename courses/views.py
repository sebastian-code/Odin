from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from students.models import CourseAssignment, User, Solution
from .models import Course, Partner, Certificate, Task


def show_course(request, course_url):
    course = get_object_or_404(Course, url=course_url)
    enable_applications = date.today() <= course.application_until
    return render(request, 'show_course.html', locals())


def show_all_courses(request):
    date_today = date.today()
    active_courses = Course.objects.filter(Q(start_time__lte=date_today) | Q(end_time__gt=date_today) | Q(end_time=None)).exclude(start_time=None)
    upcoming_courses = Course.objects.filter(Q(start_time__gt=date_today) | Q(start_time=None))
    ended_courses = Course.objects.filter(end_time__lte=date_today).exclude(start_time=None)
    return render(request, 'show_all_courses.html', locals())


def show_all_partners(request):
    partners = Partner.objects.filter(is_active=True)
    return render(request, 'show_all_partners.html', locals())


@login_required
def show_course_students(request, course_id):
    assignments = CourseAssignment.objects.filter(course=course_id, user__status=User.STUDENT)
    is_teacher_or_hr = request.user.status == User.HR or request.user.status == User.TEACHER
    if request.user.hr_of:
        interested_in_me = CourseAssignment.objects.filter(
            course=course_id,
            favourite_partners=request.user.hr_of,
            user__status=User.STUDENT
        )
    return render(request, 'show_course_students.html', locals())


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

    return render(request, 'show_certificate.html', locals())
