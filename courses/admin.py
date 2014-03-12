from django.contrib import admin
from models import Course

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'start_time',
        'end_time'
        ]

    list_display_links = ['name']

admin.site.register(Course, CourseAdmin)