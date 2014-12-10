import datetime
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.db import IntegrityError
from django.conf import settings

from .forms import UserEditForm, AddNote, VoteForPartner, AddSolutionForm, GiveFeedbackForm
from .models import CourseAssignment, UserNote, User, CheckIn, Task, Solution
from courses.models import Course, Certificate
from forum.models import Comment


def login(request):
    if request.user.is_authenticated():
        return redirect('students:user_profile')
    else:
        return auth_views.login(request, template_name='login_form.html')


@login_required
def logout(request):
    auth_views.logout(request)
    return redirect('/')


@login_required
def user_profile(request):
    current_user = request.user
    is_student = current_user.status == current_user.STUDENT
    is_hr = current_user.status == current_user.HR
    is_teacher = current_user.status == current_user.TEACHER

    assignments = CourseAssignment.objects.only('course', 'user').filter(user=current_user).select_related('course').order_by('course__name')
    certificates = Certificate.objects.only('assignment').filter(assignment__in=assignments).select_related('assignment').order_by('assignment__course__name')
    return render(request, 'profile.html', locals())


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('students:user_profile')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'edit_profile.html', locals())


@login_required
def assignment(request, id):
    assignment = get_object_or_404(CourseAssignment.objects.select_related('user', 'course'), pk=id)
    certificate = Certificate.objects.filter(assignment=assignment).first()
    comments = Comment.objects.filter(author=assignment.user).select_related('topic').order_by('topic')
    is_hr = request.user.status == User.HR
    is_student = request.user.status == User.STUDENT
    is_teacher = request.user.status == User.TEACHER

    if is_teacher or is_hr:
        notes = UserNote.objects.filter(assignment=id).select_related('author')

    if is_teacher:
        if request.method == 'POST':
            form = AddNote(request.POST, author=request.user)
            if form.is_valid():
                form.save()
                return redirect('students:assignment', id=id)
        else:
            form = AddNote(author=request.user)

    if is_student and request.user == assignment.user:
        if assignment.course.ask_for_favorite_partner:
            vote_form = VoteForPartner(instance=assignment, assignment=assignment)
            if request.method == 'POST':
                vote_form = VoteForPartner(request.POST, request.FILES, instance=assignment, assignment=assignment)
                if vote_form.is_valid():
                    vote_form.save()
                    return redirect('students:assignment', id=id)

        date_today = datetime.date.today()
        # get course.end_time if existing, else fake a date from 10 years ago
        course_end_date = datetime.date(1990, 1, 1)
        if assignment.course.end_time:
            course_end_date = assignment.course.end_time
        has_ended = date_today >= course_end_date
        has_started_working_at = len(assignment.studentstartedworkingat_set.all()) > 0
        if assignment.course.ask_for_feedback and has_ended and not has_started_working_at:
            feedback_form = GiveFeedbackForm(assignment=assignment)
            if request.method == 'POST':
                feedback_form = GiveFeedbackForm(request.POST, request.FILES, assignment=assignment)
                if feedback_form.is_valid():
                    feedback_form.save()
                    return redirect('students:assignment', id=id)

    return render(request, 'assignment.html', locals())


@csrf_exempt
@require_http_methods(['POST'])
def set_check_in(request):
    mac = request.POST['mac']
    token = request.POST['token']

    if settings.CHECKIN_TOKEN != token:
        return HttpResponse(status=511)

    student = get_object_or_404(User, mac__iexact=mac)
    try:
        checkin = CheckIn(mac=mac, student=student)
        checkin.save()
    except IntegrityError:
        return HttpResponse(status=418)

    return HttpResponse(status=200)


@csrf_exempt
def api_students(request):
    all_students = User.objects.filter(status=User.STUDENT)
    needed_data = []

    for student in all_students:
        student_courses = []
        available = CheckIn.objects.filter(date=datetime.datetime.now, student=student).count() != 0

        for assignment in student.courseassignment_set.all():
            course = {
                'name': assignment.course.name,
                'group': assignment.group_time
            }
            student_courses.append(course)

        needed_data.append({
            'name': student.get_full_name(),
            'courses': student_courses,
            'github': student.github_account,
            'available': available,
        })

    return HttpResponse(json.dumps(needed_data, ensure_ascii=False), content_type='application/json; charset=utf8')


@csrf_exempt
def api_checkins(request):
    checkins = CheckIn.objects.all()
    needed_data = []

    for checkin in checkins:
        student_courses = []

        for assignment in checkin.student.courseassignment_set.all():
            course = {
                'name': assignment.course.name,
                'group': assignment.group_time
            }
            student_courses.append(course)

        needed_data.append({
            'student_id': checkin.student.id,
            'student_name': checkin.student.get_full_name(),
            'student_courses': student_courses,
            'date': str(checkin.date),
        })

    return HttpResponse(json.dumps(needed_data, ensure_ascii=False), content_type='application/json; charset=utf8')


@login_required
def solutions(request, course_url):
    course = get_object_or_404(Course, url=course_url)
    tasks = Task.objects.select_related('solution').filter(course=course).order_by('name')
    weeks = sorted(set(map(lambda task: task.week, tasks)))
    solutions = Solution.objects.filter(task__in=tasks, user=request.user).select_related('task')

    solutions_by_task = {}
    for solution in solutions:
        solutions_by_task[solution.task] = solution

    for task in tasks:
        if task in solutions_by_task:
            task.solution = solutions_by_task[task]

    return render(request, 'solutions.html', locals())


@login_required
def assignment_solutions(request, id):
    assignment = get_object_or_404(CourseAssignment, pk=id)
    course = assignment.course
    user = assignment.user
    tasks = Task.objects.select_related('solution').filter(course=course).order_by('name')
    weeks = sorted(set(map(lambda task: task.week, tasks)))
    solutions = Solution.objects.filter(task__in=tasks, user=user).select_related('task')

    solutions_by_task = {}
    for solution in solutions:
        solutions_by_task[solution.task] = solution

    for task in tasks:
        if task in solutions_by_task:
            task.solution = solutions_by_task[task]

    return render(request, 'assignment_solutions.html', locals())


@csrf_exempt
@login_required
@require_http_methods(['POST'])
def add_solution(request):
    solution = Solution.objects.filter(
        user=request.user,
        task=request.POST['task'],
    ).first()

    if solution:
        form = AddSolutionForm(request.POST, instance=solution, user=request.user)
    else:
        form = AddSolutionForm(request.POST, user=request.user)

    if form.is_valid():
        form.save()
        return HttpResponse(status=200)

    return HttpResponse(status=422)


@csrf_exempt
@login_required
@require_http_methods(['POST'])
def toggle_assignment_activity(request, id):
    assignment = get_object_or_404(CourseAssignment, pk=id)
    user = request.user
    user_course_list = map(lambda x: x.course, user.courseassignment_set.all())
    if user.status != User.TEACHER or assignment.course not in user_course_list:
        return HttpResponse(status=403)

    assignment.is_attending = not assignment.is_attending
    assignment.save()
    return HttpResponse(status=200)
