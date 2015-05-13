# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_studentstartedworkingat_not_working'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentstartedworkingat',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True),
            preserve_default=True,
        ),
    ]
