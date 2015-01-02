from django.contrib import admin

from .models import Faq


class FaqAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
    ]

    list_display_links = ['title']

admin.site.register(Faq, FaqAdmin)
