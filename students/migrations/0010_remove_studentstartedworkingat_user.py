# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_studentstartedworkingat_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentstartedworkingat',
            name='user',
        ),
    ]
