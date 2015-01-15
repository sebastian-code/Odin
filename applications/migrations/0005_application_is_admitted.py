# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0004_auto_20150115_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='is_admitted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
