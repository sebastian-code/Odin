# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_data(apps, schema_editor):
    Solution = apps.get_model("students", "Solution")
    CourseAssignment = apps.get_model("students", "CourseAssignment")

    solutions = Solution.objects.all()

    for solution in solutions:
        assignment = CourseAssignment.objects.get(user=solution.user, course=solution.task.course)
        solution.assignment = assignment
        solution.save()


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='assignment',
            field=models.ForeignKey(default=1, to='students.CourseAssignment'),
            preserve_default=False,
        ),
        migrations.RunPython(migrate_data)
    ]
