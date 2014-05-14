from django.db import models
from students.models import User

class Category(models.Model):
    title = models.CharField(blank=False, max_length=128)
    text = models.CharField(blank=False, max_length=512)
    ordering = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
    
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('ordering',)

class Topic(models.Model):
    title = models.CharField(blank=False, max_length=128)
    text = models.TextField(blank=False)
    author = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    
    def __unicode__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField(blank=False)
    author = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)
