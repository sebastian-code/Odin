from django.contrib import admin

from adminsortable.admin import SortableAdminMixin

from .models import Category, Topic, Comment


class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = [
        'id',
        'title',
    ]

    list_display_links = ['title']

admin.site.register(Category, CategoryAdmin)


class TopicAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
    ]

    list_display_links = ['title']

admin.site.register(Topic, TopicAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'topic',
    ]

    list_display_links = ['author']

admin.site.register(Comment, CommentAdmin)
