from django.contrib import admin
from .models import Application


class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'student',
        'course',
        'date',
    ]

    list_filter = ('course',)

admin.site.register(Application, ApplicationAdmin)
