from django.core.urlresolvers import reverse
from django.db import models

from tinymce import models as tinymce_models


class Course(models.Model):
    description = tinymce_models.HTMLField(blank=False)
    git_repository = models.CharField(blank=True, max_length=256)
    image = models.ImageField(upload_to='courses_logoes', blank=True, default='')
    name = models.CharField(blank=False, max_length=64)
    partner = models.ManyToManyField('Partner', null=True, blank=True)
    short_description = models.CharField(blank=True, max_length=300)
    show_on_index = models.BooleanField(default=False)

    application_until = models.DateField()
    applications_url = models.URLField(blank=True)
    ask_for_favorite_partner = models.BooleanField(default=False)
    ask_for_feedback = models.BooleanField(default=False)
    end_time = models.DateField(blank=True, null=True)
    next_season_mail_list = models.URLField(blank=True)
    SEO_description = models.CharField(blank=False, max_length=255)
    SEO_title = models.CharField(blank=False, max_length=255)
    start_time = models.DateField(blank=True, null=True)
    url = models.SlugField(max_length=80, unique=True)

    def __unicode__(self):
        return unicode(self.name)


class Partner(models.Model):
    description = tinymce_models.HTMLField(blank=False)
    facebook = models.URLField(blank=True)
    is_active = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='partner_logoes', blank=True, default='')
    name = models.CharField(max_length=128)
    ordering = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
    twitter = models.URLField(blank=True)
    website = models.URLField(blank=True)

    class Meta:
        ordering = ('ordering',)

    def __unicode__(self):
        return unicode(self.name)


class Task(models.Model):
    course = models.ForeignKey(Course)
    deadline = models.DateTimeField(null=True, blank=True)
    description = models.URLField()
    is_exam = models.BooleanField(default=False)
    name = models.CharField(max_length=128)
    week = models.CharField(max_length=10, blank=False)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'description'),)


class WeeklyCommit(models.Model):
    commits_count = models.IntegerField(default=0)


class Certificate(models.Model):
    assignment = models.OneToOneField('students.CourseAssignment')
    issues_closed = models.IntegerField(default=0)
    issues_opened = models.IntegerField(default=0)
    total_commits = models.IntegerField(default=0)
    weekly_commits = models.ManyToManyField(WeeklyCommit)

    def get_absolute_url(self):
        return reverse('courses:show_certificate', args=[str(self.assignment.id)])
