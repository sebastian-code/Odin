# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_solution_assignment'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='assignment',
            field=models.OneToOneField(null=True, to='students.CourseAssignment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='certificate',
            name='weekly_commits',
            field=models.ManyToManyField(to='courses.WeeklyCommit'),
            preserve_default=True,
        ),
    ]
