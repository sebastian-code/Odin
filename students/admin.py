from django.contrib import admin
from models import User, CourseAssignment, UserNote


class UsersAdmin(admin.ModelAdmin):
    list_display = [
        'faculty_number',
        'first_name',
        'last_name',
    ]

    list_display_links = ['faculty_number']

admin.site.register(User, UsersAdmin)


class CourseAssignmentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'course',
        'points',
    ]

    list_display_links = ['user']

admin.site.register(CourseAssignment, CourseAssignmentAdmin)


class UserNoteAdmin(admin.ModelAdmin):
    list_display = [
        'text',
        'assignment',
    ]

admin.site.register(UserNote, UserNoteAdmin)
