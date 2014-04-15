from django.contrib import admin
from pagedown.widgets import AdminPagedownWidget
from models import Faq
from django.db import models


class FaqAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
    ]

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
    
    list_display_links = ['title']

admin.site.register(Faq, FaqAdmin)
