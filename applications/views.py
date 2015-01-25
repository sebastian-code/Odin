from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


from .forms import ApplicationForm, AddApplicationSolutionForm
from .models import Application, ApplicationSolution, ApplicationTask
from courses.models import Course
from students.models import CourseAssignment


def apply(request):
    current_user = request.user

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('applications:thanks')

    form = ApplicationForm()
    form_courses = form.fields['course'].queryset

    if not form_courses:
        error_message = 'За момента няма курсове, за които да се запишете. Следете блога на HackBulgaria\n\
                        или вижте някои от курсовете досега.'
        return render(request, 'generic_error.html', {'error_message': error_message})

    if form_courses and current_user.is_authenticated():
        existing_applications = Application.objects.select_related('course').filter(student=current_user, course__in=form_courses)

        if existing_applications:
            courses = [str(obj.course) for obj in existing_applications]
            error_message = 'Вие вече сте кандидатствали за {0}'.format(', '.join(courses))
            return render(request, 'generic_error.html', {'error_message': error_message})

        try:
            last_assignment = CourseAssignment.objects.filter(user=current_user).exclude(course__in=form_courses).latest('course__end_time')
        except CourseAssignment.DoesNotExist:
            last_assignment = None

        if last_assignment and last_assignment.is_attending is False:
            header_text = 'Изглежда, че не сте завършили последният записан курс при нас.\nЩе се наложи да кандидатствате отново за следващият.'
        elif last_assignment and last_assignment.is_attending:
            data = current_user.__dict__  # efficient
            data['name'] = current_user.get_full_name()
            form = ApplicationForm(data)  # should think of a way to inject data into existing form

        return render(request, 'apply.html', locals())

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
