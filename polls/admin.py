from django.contrib import admin

from models import Poll, Question, Answer, Choice


class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_question_list']
    list_filter = ('is_active',)

admin.site.register(Poll, PollAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user_full_name', 'user_email', 'choice']
    list_filter = ('user',)

    def user_full_name(self, instance):
        return unicode(instance.user)

    def user_email(self, instance):
        return instance.user.email

admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question)
admin.site.register(Choice)
