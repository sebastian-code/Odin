# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20150203_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='studies_at',
            field=models.CharField(blank=True, null=True, max_length='110'),
            preserve_default=True,
        ),
    ]
