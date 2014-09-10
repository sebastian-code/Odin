from django.contrib import admin

from models import PartnerStats


class PartnerStatsAdmin(admin.ModelAdmin):
    list_display = [
        'partner',
        'money_spent'
    ]

admin.site.register(PartnerStats, PartnerStatsAdmin)
