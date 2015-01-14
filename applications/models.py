from django.db import models


class Application(models.Model):
    student = models.ForeignKey('students.User')
    course = models.ForeignKey('courses.Course')
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return 'Application for course <{0}> by <{1}>'.format(self.course, self.student)


class ApplicationTask(models.Model):
    course = models.ForeignKey('courses.Course')
    title = models.CharField(blank=False, max_length=255)
    url = models.URLField()


class ApplicationSolution(models.Model):
    task = models.ForeignKey(ApplicationTask)
    user = models.ForeignKey('students.User')
