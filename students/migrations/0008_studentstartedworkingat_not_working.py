# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentstartedworkingat',
            name='not_working',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
