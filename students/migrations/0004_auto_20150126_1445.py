# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20150126_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseassignment',
            name='favourite_partners',
            field=models.ManyToManyField(to='courses.Partner', null=True, blank=True),
            preserve_default=True,
        ),
    ]
