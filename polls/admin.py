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


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'text', 'is_free']
    list_filter = ('question',)

admin.site.register(Choice, ChoiceAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'free_text_enabled']

admin.site.register(Question, QuestionAdmin)
