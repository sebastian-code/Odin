# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20150203_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='works_at',
            field=models.CharField(blank=True, max_length='110', null=True),
            preserve_default=True,
        ),
    ]
