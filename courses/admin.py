from django.contrib import admin
from models import Course, Partner


# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]

    list_display_links = ['name']

admin.site.register(Course, CourseAdmin)

class PartnerAdmin(admin.ModelAdmin):
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
