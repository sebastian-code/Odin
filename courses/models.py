from django.core.urlresolvers import reverse
from django.db import models

from tinymce import models as tinymce_models


class Course(models.Model):
    name = models.CharField(blank=False, max_length=64)
    short_description = models.CharField(blank=True, max_length=300)
    description = tinymce_models.HTMLField(blank=False)
    image = models.ImageField(upload_to="courses_logoes", null=True, blank=True)
    git_repository = models.CharField(blank=True, max_length=256)
    show_on_index = models.BooleanField(default=False)
    partner = models.ManyToManyField('Partner', null=True, blank=True)

    applications_url = models.URLField(null=True, blank=True)
    application_until = models.DateField()
    next_season_mail_list = models.URLField(null=True, blank=True)

    start_time = models.DateField(blank=True, null=True)
    end_time = models.DateField(blank=True, null=True)

    SEO_title = models.CharField(blank=False, max_length=255)
    SEO_description = models.CharField(blank=False, max_length=255)
    url = models.SlugField(max_length=80, unique=True)

    ask_for_favorite_partner = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Partner(models.Model):
    name = models.CharField(max_length=128)
    logo = models.ImageField(upload_to="partner_logoes", null=True, blank=True)
    description = tinymce_models.HTMLField(blank=False)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    ordering = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('ordering',)

    def __unicode__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=128)
    description = models.URLField()
    course = models.ForeignKey(Course)
    is_exam = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    week = models.CharField(max_length=10, blank=False, null=False)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        unique_together = (('name', 'description', 'course', 'is_exam', 'week'),)


class WeeklyCommit(models.Model):
    commits_count = models.IntegerField(default=0)


class Certificate(models.Model):
    assignment = models.ForeignKey('students.CourseAssignment', unique=True)
    weekly_commits = models.ManyToManyField(WeeklyCommit)
    issues_closed = models.IntegerField(default=0)
    issues_opened = models.IntegerField(default=0)
    total_commits = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('courses:show-certificate', args=[str(self.assignment.id)])
