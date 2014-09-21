from django.contrib import admin

from models import Poll, Question, Answer, Choice


class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_question_list']
    list_filter = ('is_active',)

admin.site.register(Poll, PollAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Choice)
