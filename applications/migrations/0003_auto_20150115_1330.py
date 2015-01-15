# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_auto_20150113_1309'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicationsolution',
            old_name='user',
            new_name='student',
        ),
        migrations.RenameField(
            model_name='applicationtask',
            old_name='url',
            new_name='description',
        ),
        migrations.AddField(
            model_name='applicationsolution',
            name='repo',
            field=models.URLField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
