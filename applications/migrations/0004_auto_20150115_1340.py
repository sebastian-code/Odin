# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_auto_20150115_1330'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicationtask',
            old_name='title',
            new_name='name',
        ),
    ]
