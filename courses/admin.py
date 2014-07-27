from django.contrib import admin
from adminsortable.admin import SortableAdminMixin

from models import Course, Partner


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
