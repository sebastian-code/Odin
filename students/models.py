from django.db import models
from django.contrib.auth.models import AbstractUser
from courses.models import Course


class User(AbstractUser):
    faculty_number = models.CharField(max_length=8)
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    github_account = models.URLField(null=True, blank=True)
    linkedin_account = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True)
    courses = models.ManyToManyField(Course, through='CourseAssignment')

    AbstractUser._meta.get_field('email')._unique = True
    AbstractUser.REQUIRED_FIELDS.remove('email')
    
    USERNAME_FIELD = 'email'
    
    def __unicode__(self):
        return unicode(self.username)


class CourseAssignment(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    points = models.PositiveIntegerField(default='0')
    
    class Meta:
        unique_together = ('user', 'course')

    def __unicode__(self):
        return unicode('{} - {}'.format(self.user, self.course))


class UserNote(models.Model):
    text = models.TextField(blank=True)
    assignment = models.ForeignKey(CourseAssignment)
    author = models.ForeignKey(User, null=True, blank=True)
    post_time = models.DateTimeField(auto_now=True)
