from django.db import models

from students.models import CourseAssignment


class Application(models.Model):
    course = models.ForeignKey('courses.Course')
    date = models.DateField(auto_now=True)
    is_admitted = models.BooleanField(default=False)
    student = models.ForeignKey('students.User')

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return 'Application for course <{0}> by <{1}>'.format(self.course, self.student)

    def get_assignment(self):
        try:
            return CourseAssignment.objects.get(user=self.student, course=self.course)
        except CourseAssignment.DoesNotExist:
            return None

    def get_assignment_url(self):
        try:
            assignment = CourseAssignment.objects.get(user=self.student, course=self.course)
            return assignment.get_absolute_url()
        except CourseAssignment.DoesNotExist:
            return None

    def email_student(self, subject, message):
        self.student.send_email(subject, message)

    def is_finished(self):
        tasks = self.course.applicationtask_set.all()
        solutions = ApplicationSolution.objects.filter(student=self.student, task__in=tasks)
        # This is the most ugly hardcode ever done in the history programming...
        if self.course.id == 12 or self.course.id == 14:
            if solutions.count() == 3:
                return True

        if len(tasks) == solutions.count():
            return True
        return False


class ApplicationTask(models.Model):
    course = models.ForeignKey('courses.Course')
    description = models.URLField()
    name = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.name


class ApplicationSolution(models.Model):
    repo = models.URLField(blank=True, null=True)
    student = models.ForeignKey('students.User')
    task = models.ForeignKey(ApplicationTask)

    def __str__(self):
        return '{0} - {1}'.format(self.student, self.task)
