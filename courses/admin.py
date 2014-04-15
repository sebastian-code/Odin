from django.contrib import admin
from pagedown.widgets import AdminPagedownWidget
from models import Course
from django.db import models


# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'start_time',
        'end_time'
    ]

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    list_display_links = ['name']

admin.site.register(Course, CourseAdmin)
