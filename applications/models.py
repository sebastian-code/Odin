from django.db import models

from students.models import User
from courses.models import Course


class Application(models.Model):
    student = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course')
