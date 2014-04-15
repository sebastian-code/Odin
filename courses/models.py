from django.db import models


class Course(models.Model):
    name = models.CharField(blank=False, max_length=64)
    short_description = models.CharField(blank=True, max_length=300)
    description = models.TextField(blank=False)
    image = models.ImageField(upload_to="courses_logoes", null=True, blank=True)
    git_repository = models.CharField(blank=True, max_length=256)
    show_on_index = models.BooleanField(default=False)
    enable_applications = models.BooleanField(default=False)
    applications_url = models.URLField(null=True, blank=True)
    start_time = models.DateField()
    end_time = models.DateField()

    SEO_title = models.CharField(blank=False, max_length=255)
    SEO_description = models.CharField(blank=False, max_length=255)
    url = models.SlugField(max_length=80, unique=True)

    def __unicode__(self):
        return self.name
