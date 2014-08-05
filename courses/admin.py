from django.contrib import admin

from models import Certificate, Course, Partner, Task

from adminsortable.admin import SortableAdminMixin


# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]

    list_display_links = ['name']

admin.site.register(Course, CourseAdmin)


class PartnerAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'logo',
        'facebook',
        'twitter',
        'website',
    ]

    list_display_links = ['name']

admin.site.register(Partner, PartnerAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'week',
    ]

    list_display_links = ['name']

admin.site.register(Task, TaskAdmin)


class CertificateAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'assignment',
        'issues_closed',
        'issues_opened',
        'total_commits'
    ]
    list_display_links = ['assignment']

admin.site.register(Certificate, CertificateAdmin)
