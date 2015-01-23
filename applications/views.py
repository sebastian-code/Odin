from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


from .forms import ApplicationForm, AddApplicationSolutionForm
from .models import Application, ApplicationSolution, ApplicationTask
from courses.models import Course


def apply(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('applications:thanks')

    form = ApplicationForm()
    return render(request, 'apply.html', locals())


def thanks(request):
    return render(request, 'thanks.html', locals())


@login_required
def show_submitted_applications(request, course_url):
    current_user = request.user

    if not current_user.is_teacher():
        return HttpResponseForbidden()

    course = get_object_or_404(Course, url=course_url)
    applications = Application.objects.filter(course=course)
    return render(request, 'show_submitted_applications.html', locals())


@csrf_exempt
@login_required
@require_http_methods(['POST'])
def add_solution(request):
    solution = ApplicationSolution.objects.filter(
        user=request.user,
        task=request.POST['task'],
    ).first()

    if solution:
        form = AddApplicationSolutionForm(request.POST, instance=solution, user=request.user)
    else:
        form = AddApplicationSolutionForm(request.POST, user=request.user)

    if form.is_valid():
        form.save()
        return HttpResponse(status=200)

    return HttpResponse(status=422)


@login_required
def solutions(request, course_url):
    course = get_object_or_404(Course, url=course_url)
    tasks = ApplicationTask.objects.select_related('solution').filter(course=course).order_by('name')

    solutions = ApplicationSolution.objects.filter(task__in=tasks, student=request.user).select_related('task')

    solutions_by_task = {}
    for solution in solutions:
        solutions_by_task[solution.task] = solution

    for task in tasks:
        if task in solutions_by_task:
            task.solution = solutions_by_task[task]

    header_text = 'Задачи за прием: {0}'.format(course.get_course_with_deadlines())
    return render(request, 'solutions.html', locals())
