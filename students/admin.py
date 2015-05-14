from django.contrib import admin

from students.models import User, CourseAssignment, EducationInstitution, UserNote, CheckIn, HrLoginLog, Solution, StudentStartedWorkingAt


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
        'is_attending',
        'is_online'
    ]

    list_filter = ('course', 'group_time', 'is_attending', 'is_online')
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
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


class StudentStartedWorkingAtAdmin(admin.ModelAdmin):
    list_display = [
        'assignment',
        'partner',
        'partner_name',
        'not_working'
    ]
    list_filter = ('partner', 'not_working')

admin.site.register(StudentStartedWorkingAt, StudentStartedWorkingAtAdmin)

admin.site.register(Solution, SolutionAdmin)
admin.site.register(EducationInstitution)
