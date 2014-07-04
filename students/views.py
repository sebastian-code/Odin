from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views
from .forms import UserEditForm, AddNote
from .models import CourseAssignment, UserNote, User, CheckIn
from django.http import HttpResponse
from django.utils import simplejson

import datetime


def login(request):
    if request.user.is_authenticated():
        return redirect('profile')
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

    return render(request, "assignment.html", locals())


@csrf_exempt
def set_check_in(request):
    if request.method == 'POST':
        mac = request.POST['mac']
        
        student = get_object_or_404(User, mac__iexact=mac)

        checkin = CheckIn(mac=mac, student=student)
        checkin.save()

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
    print(checkins)
    return HttpResponse(simplejson.dumps(checkins, ensure_ascii=False), content_type = 'application/json; charset=utf8')