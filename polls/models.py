from django.db import models

from students.models import User


class Question(models.Model):
    free_text_enabled = models.BooleanField(default=False)
    title = models.CharField(blank=True, max_length=256)

    def __unicode__(self):
        return unicode(self.title)


class Choice(models.Model):
    is_free = models.BooleanField(default=False)
    question = models.ForeignKey(Question)
    text = models.CharField(blank=True, max_length=256)

    def __unicode__(self):
        return unicode(self.text)


class Answer(models.Model):
    choice = models.ForeignKey(Choice)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.choice.text)


class Poll(models.Model):
    title = models.CharField(max_length=256)
    question = models.ManyToManyField(Question)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.title)

    def user_has_answered(self, user):
        result = False
        for question in self.question.all():
            result = any(choice.answer_set.filter(user=user).count() > 0 for choice in question.choice_set.all())
        return result
