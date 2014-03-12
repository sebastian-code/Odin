from django.db import models


class Course(models.Model):
    name = models.CharField(blank=False, max_length=64)
    description = models.TextField(blank=False)
    image = models.ImageField(upload_to="courses_logoes", null=True, blank=True)
    start_time = models.DateField()
    end_time = models.DateField()

    def __unicode__(self):
        return self.name