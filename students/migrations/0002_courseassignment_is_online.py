# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseassignment',
            name='is_online',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
