from django.db import models

from students.models import User


class Question(models.Model):
    free_text_enabled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
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

    def __unicode__(self):
        return unicode(self.title)
