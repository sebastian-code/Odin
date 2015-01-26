from django.db import models

from students.models import User


class Category(models.Model):
    title = models.CharField(blank=False, max_length=128)
    text = models.CharField(blank=False, max_length=512)
    ordering = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('ordering',)


class Topic(models.Model):
    title = models.CharField(blank=False, max_length=128)
    text = models.TextField(blank=False)
    author = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(blank=False)
    author = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)

    def __str__(self):
        return self.text
