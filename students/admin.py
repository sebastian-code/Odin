from django.contrib import admin
from models import User, CourseAssignment, UserNote, CheckIn


class UsersAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
        'mac',
        'get_courses'
    ]
    list_display_links = ['email']


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


class CheckInAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'mac',
        'student',
        'date',

    ]

admin.site.register(CheckIn, CheckInAdmin)
