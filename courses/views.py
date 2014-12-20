from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

from statistics.helpers import division_or_zero
from students.models import CourseAssignment, User, Solution
from .models import Course, Partner, Certificate, Task


def show_course(request, course_url):
    course = get_object_or_404(Course, url=course_url)
    enable_applications = date.today() <= course.application_until
    return render(request, 'show_course.html', locals())


def show_all_courses(request):
    date_today = date.today()
    active_courses = Course.objects.filter(Q(start_time__lte=date_today, end_time__gt=date_today) | Q(end_time=None)).exclude(start_time=None)
    upcoming_courses = Course.objects.filter(Q(start_time__gt=date_today) | Q(start_time=None))
    ended_courses = Course.objects.filter(end_time__lte=date_today).exclude(start_time=None)
    return render(request, 'show_all_courses.html', locals())


def show_all_partners(request):
    partners = Partner.objects.filter(is_active=True)
    return render(request, 'show_all_partners.html', locals())


@login_required
def show_course_students(request, course_url):
    current_user = request.user
    course = get_object_or_404(Course, url=course_url)
    assignments = CourseAssignment.objects.only('id', 'user', 'course').filter(
        course=course,
        user__status=User.STUDENT
    ).select_related('user', 'certificate').prefetch_related('usernote_set', 'usernote_set__author').order_by('-is_attending')


    is_teacher_or_hr = current_user.is_hr() or current_user.is_teacher()

    if current_user.hr_of:
        interested_in_me = CourseAssignment.objects.filter(
            course=course,
            favourite_partners=current_user.hr_of,
            user__status=User.STUDENT
        )

        assignments = sorted(assignments, key = lambda x: (not x.is_attending, not x in interested_in_me))

    return render(request, 'show_course_students.html', locals())


def show_certificate(request, assignment_id):
    certificate = get_object_or_404(Certificate, assignment=assignment_id)
    assignment = certificate.assignment
    user = assignment.user
    course = assignment.course
    tasks = Task.objects.filter(course=course)
    solutions = Solution.objects.filter(task__in=tasks, user=user)

    solutions_by_task = {}
    for solution in solutions:
        solutions_by_task[solution.task.id] = solution

    for task in tasks:
        if task.id in solutions_by_task:
            task.solution = solutions_by_task[task.id]
    percent = round(division_or_zero(solutions.count(), tasks.count()) * 100, 2)
    return render(request, 'show_certificate.html', locals())


@login_required
def show_submitted_solutions(request, course_url):
    current_user = request.user

    if not current_user.is_teacher():
        return HttpResponseForbidden()

    course = get_object_or_404(Course, url=course_url)
    tasks = Task.objects.filter(course=course).select_related('solution').order_by('name')
    weeks = sorted(set(map(lambda task: task.week, tasks)))
    solutions = Solution.objects.filter(task__in=tasks).select_related('task')

    solutions_by_task = {}
    for solution in solutions:
        solutions_by_task[solution.task] = solution

    for task in tasks:
        if task in solutions_by_task:
            task.solution = solutions_by_task[task]

    return render(request, 'show_submitted_solutions.html', locals())
