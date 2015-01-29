from django.conf import settings
from django.contrib import admin
from django.contrib import messages as dj_messages
from django.contrib.admin import helpers
from django.core.mail import send_mass_mail
from django.template import Context, Template
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.template.response import TemplateResponse

from applications.models import Application, ApplicationTask, ApplicationSolution
from students.models import CourseAssignment


class ApplicationAdmin(admin.ModelAdmin):
    actions = ['admit_applications']
    list_display = [
        'student',
        'course',
        'date',
    ]
    list_filter = ('course',)

    def admit_applications(self, request, queryset):

        if request.POST.get('post'):
            n = queryset.count()
            if n:
                mails = []
                form_message_template = request.POST.get('message_template')
                template = Template(form_message_template) if form_message_template else get_template('admit_template.html')
                courses = [obj.course for obj in queryset]
                admitted_students = CourseAssignment.objects.filter(course__in=courses).only('user')

                for obj in queryset:
                    student = obj.student
                    if student in admitted_students:
                        continue
                    course = obj.course
                    CourseAssignment.objects.create(
                        course=course,
                        user=student,
                        group_time=CourseAssignment.EARLY,
                        )
                    context = Context({
                        'course': course,
                        'course_name': course.name,
                        'course_start_date': course.start_time,
                        'student': student,
                        'student_name': student.get_full_name(),
                    })
                    message = template.render(context)
                    subject = 'HackBulgaria admission for {0}'.format(course)
                    mails.append((subject, message, settings.DEFAULT_FROM_EMAIL, (student.email,)))

                send_mass_mail(mails)
                students = (obj.student for obj in queryset)
                names = ','.join((obj.get_full_name() for obj in students))
                self.message_user(
                    request, 'You successfully admitted and emailed {0}'.format(
                        names),
                    dj_messages.SUCCESS)
            return None

        default_text = render_to_string('admit_template.html')
        opts = self.model._meta
        if len(queryset) == 1:
            objects_name = opts.verbose_name
        else:
            objects_name = opts.verbose_name_plural

        context = {
            'title': "Are you sure?",
            'objects_name': objects_name,
            'default_text': default_text,
            'queryset': queryset,
            'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        }

        return TemplateResponse(request, 'admit_applications.html',
                                context, current_app=self.admin_site.name)

admin.site.register(Application, ApplicationAdmin)
admin.site.register(ApplicationTask)
admin.site.register(ApplicationSolution)
