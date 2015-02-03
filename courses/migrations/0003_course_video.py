# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20150106_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='video',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
    ]
