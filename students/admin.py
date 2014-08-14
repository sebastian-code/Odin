from django.contrib import admin

from models import User, CourseAssignment, UserNote, CheckIn, HrLoginLog, Solution


class UsersAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
        'mac',
        'get_courses',
        'works_at',
        'status',
    ]
    list_display_links = ['email']

    list_filter = ('works_at', 'status')

admin.site.register(User, UsersAdmin)


class CourseAssignmentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'course',
        'group_time',
        'get_favourite_partners',
        'cv',
    ]

    list_filter = ('course', 'group_time')

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


class HrLoginLogAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'date',
    ]

admin.site.register(HrLoginLog, HrLoginLogAdmin)


class SolutionAdmin(admin.ModelAdmin):
    list_display = [
        'task',
        'user',
        'repo'
    ]
    list_display_links = ['repo']
    list_filter = ('task__course', 'user')

admin.site.register(Solution, SolutionAdmin)
