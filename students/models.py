from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    faculty_number = models.CharField(max_length=8)
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    github_account = models.URLField(null=True, blank=True)
    linkedin_account = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True)


    def __unicode__(self):
        return unicode(self.username)
