from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


from applications.forms import ApplicationForm, AddApplicationSolutionForm, ExistingUserApplicationForm, ExistingAttendingUserApplicationForm
from applications.models import Application, ApplicationSolution, ApplicationTask
from courses.models import Course
from students.models import CourseAssignment


NO_COURSES_TO_APPLY_FOR_ERROR = 'За момента няма курсове, за които да се запишете. Следете блога на HackBulgaria\n\
              или вижте някои от курсовете досега.'
HASNT_ATTENDED_LAST_ENROLLED_COURSE_ERROR = 'Тъй като не си завършил успешно курс в Хак България ще трябва да кандидатстваш отново. Попълни формата за кандидатстване и ще получиш имейл със следващите стъпки.'
HAS_ATTENDED_LAST_ENROLLED_COURSE_MESSAGE = 'Поздравления! Ти успешно си завършил поне един курс в Хак България и можеш да избереш следващ , в който да продължиш. От теб не се изисква да решаваш задачи за кандидатстване, нито пък да се явиш на интервю.'
ALREADY_ADMITTED_IN_COURSE_ERROR = 'Вие вече сте приет в {0}! :)'
ALREADY_APPLIED_FOR_COURSE_ERROR = 'Вие вече сте кандидатствали за {0}'


def apply(request):
    current_user = request.user
    latest_assignment = None

    if current_user.is_authenticated():
        try:
            latest_assignment = CourseAssignment.objects.filter(user=current_user).latest('course__end_time')
        except CourseAssignment.DoesNotExist:
            pass

    if request.method == 'POST':
        attending_user = False
        if latest_assignment and latest_assignment.is_attending:
            form = ExistingAttendingUserApplicationForm(data=request.POST, user=current_user)
            attending_user = True
        elif current_user.is_authenticated():
            form = ExistingUserApplicationForm(data=request.POST, user=current_user)
        else:
            form = ApplicationForm(data=request.POST)
        if form.is_valid():
            form.save()
            if attending_user:
                return redirect('applications:thanks_user')

            return redirect('applications:thanks')
        return render(request, 'apply.html', locals())

    if current_user.is_authenticated():
        form = ExistingUserApplicationForm(data=request.POST or None, user=current_user)
    else:
        form = ApplicationForm()

    form_courses = form.fields['course'].queryset
    if not form_courses:
        error_message = NO_COURSES_TO_APPLY_FOR_ERROR
        return render(request, 'generic_error.html', {'error_message': error_message})
    elif latest_assignment and latest_assignment.course in form_courses:
        error_message = ALREADY_ADMITTED_IN_COURSE_ERROR.format(latest_assignment.course)
        return render(request, 'generic_error.html', {'error_message': error_message})

    existing_applications = Application.objects.filter(student=current_user.pk, course__in=form_courses)
    if existing_applications:
        courses = [str(obj.course) for obj in existing_applications]
        error_message = ALREADY_APPLIED_FOR_COURSE_ERROR .format(', '.join(courses))
        return render(request, 'generic_error.html', {'error_message': error_message})

    if latest_assignment and not latest_assignment.is_attending:
        header_text = HASNT_ATTENDED_LAST_ENROLLED_COURSE_ERROR
    elif latest_assignment and latest_assignment.is_attending:
        header_text = HAS_ATTENDED_LAST_ENROLLED_COURSE_MESSAGE
        form = ExistingAttendingUserApplicationForm(data=request.POST or None, user=current_user)
    return render(request, 'apply.html', locals())


def thanks(request):
    return render(request, 'thanks.html', locals())


def thanks_user(request):
    return render(request, 'thanks_user.html', locals())


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
        student=request.user,
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
    tasks = ApplicationTask.objects.select_related('course').filter(course=course).order_by('name')
    solutions = ApplicationSolution.objects.select_related('task').filter(task__in=tasks, student=request.user)

    solutions_by_task = {}
    for solution in solutions:
        solutions_by_task[solution.task] = solution

    for task in tasks:
        if task in solutions_by_task:
            task.solution = solutions_by_task[task]

    header_text = 'Задачи за прием: {0}'.format(course.get_course_with_deadlines())
    return render(request, 'admission_solutions.html', locals())
