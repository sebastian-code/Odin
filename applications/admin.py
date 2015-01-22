from django.conf import settings
from django.contrib import admin
from django.contrib import messages as dj_messages
from django.contrib.admin import helpers
from django.core.mail import send_mass_mail
from django.template import Context, Template
from django.template.loader import get_template
from django.template.response import TemplateResponse

from .models import Application


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

                for obj in queryset:
                    course = obj.course
                    student = obj.student

                    context = Context({
                        'course': obj.course,
                        'course_name': course.name,
                        'course_start_date': course.start_time,
                        'student': obj.student,
                        'student_name': obj.student.get_full_name(),
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

        opts = self.model._meta
        if len(queryset) == 1:
            objects_name = opts.verbose_name
        else:
            objects_name = opts.verbose_name_plural

        context = {
            'title': "Are you sure?",
            'objects_name': objects_name,
            'queryset': queryset,
            'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        }

        return TemplateResponse(request, 'admit_applications.html',
                                context, current_app=self.admin_site.name)

admin.site.register(Application, ApplicationAdmin)
