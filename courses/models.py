from django.db import models


class Course(models.Model):
    name = models.CharField(blank=False, max_length=64)
    description = models.TextField(blank=False)
    image = models.ImageField(upload_to="courses_logoes", null=True, blank=True)
    git_repository = models.CharField(blank=True, max_length=256)
    show_on_index = models.BooleanField(default=False)
    enable_applications = models.BooleanField(default=False)
    applications_url = models.URLField(null=True, blank=True)
    start_time = models.DateField()
    end_time = models.DateField()

    def __unicode__(self):
        return self.name