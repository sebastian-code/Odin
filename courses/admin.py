from django.contrib import admin

from adminsortable.admin import SortableAdminMixin

from models import Certificate, Course, Partner, Task


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
    list_filter = ('is_active',)
    list_display_links = ['name']

admin.site.register(Partner, PartnerAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'week',
        'description',
    ]
    list_filter = ('course', 'week',)
    list_display_links = ['name']
    search_fields = ('name',)
    ordering = ('week', 'name')

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
    list_filter = ['assignment__course']

admin.site.register(Certificate, CertificateAdmin)
