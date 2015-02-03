# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20150129_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='studies_at',
            field=models.CharField(default='', max_length='110', blank=True),
            preserve_default=False,
        ),
    ]
