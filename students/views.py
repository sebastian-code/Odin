from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views
from django.http import HttpResponse
from django.db import IntegrityError
from django.utils import simplejson
from django.conf import settings

from .forms import UserEditForm, AddNote, VoteForPartner
from .models import CourseAssignment, UserNote, User, CheckIn
from forum.models import Comment

import datetime


def login(request):
    if request.user.is_authenticated():
        return redirect('students:user-profile')
    else:
        return views.login(request, template_name='login_form.html')


def logout(request):
    views.logout(request)
    return redirect('/')


def user_profile(request):
    return render(request, "profile.html", locals())


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('students:user-profile')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'edit_profile.html', locals())


@login_required
def assignment(request, id):
    assignment = get_object_or_404(CourseAssignment, pk=id)
    is_teacher = request.user.status == User.TEACHER
    is_hr = request.user.status == User.HR
    is_student = request.user.status == User.STUDENT

    comments = Comment.objects.filter(author=assignment.user).order_by('topic').all()

    if is_teacher or is_hr:
        notes = UserNote.objects.filter(assignment=id)
    
    if is_teacher:
        if request.method == 'POST':
            form = AddNote(request.POST)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.author = request.user
                submission.save()
                return redirect('students:assignment', id=id)
        else:
            form = AddNote()

    if is_student and assignment.course.ask_for_favorite_partner and request.user == assignment.user:
        vote_form = VoteForPartner(instance=assignment, assignment=assignment)
        if request.method == 'POST':
            vote_form = VoteForPartner(request.POST, request.FILES, instance=assignment, assignment=assignment)
            if vote_form.is_valid():
                vote_form.save()
                return redirect('students:assignment', id=id)

    return render(request, "assignment.html", locals())


@csrf_exempt
def set_check_in(request):
    if request.method == 'POST':
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
    all_students = User.objects.filter(status=User.STUDENT).all()
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

    return HttpResponse(simplejson.dumps(needed_data, ensure_ascii=False), content_type = 'application/json; charset=utf8')


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
            "student_id": checkin.student.id,
            "student_name": checkin.student.get_full_name(),
            "student_courses": student_courses,
            "date": str(checkin.date),
        })

    return HttpResponse(simplejson.dumps(needed_data, ensure_ascii=False), content_type = 'application/json; charset=utf8')
