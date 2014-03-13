from django.contrib import admin
from models import User

# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = [
        'faculty_number',
        'first_name',
        'last_name',
    ]

    list_display_links = ['faculty_number']

admin.site.register(User, UsersAdmin)