from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import helpers
from django.core.mail import send_mass_mail
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
                students = [obj.student.get_full_name() for obj in queryset]
                students = ','.join(students)
                self.message_user(
                    request, 'You successfully admitted and emailed {0}'.format(
                        students),
                    messages.SUCCESS)
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
