from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404  
from django.contrib.auth import views
from .forms import UserEditForm, AddNote
from .models import CourseAssignment, UserNote, User, CheckIn
from django.http import HttpResponse
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
    is_teacher = request.user.has_perm('student.add_courseassignment')

    if is_teacher:
        notes = UserNote.objects.filter(assignment=id)
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
        
        student = get_object_or_404(User, mac=mac)

        day = datetime.timedelta(days=1)
        checkin = CheckIn(mac=mac, student=student, date=datetime.date.today() - day)
        checkin.save()

        return HttpResponse(status=200)