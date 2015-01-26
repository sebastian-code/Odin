# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20150115_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationInstitution',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='studies_at',
            field=models.ForeignKey(blank=True, to='students.EducationInstitution', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='courseassignment',
            name='favourite_partners',
            field=models.ManyToManyField(blank=True, to='courses.Partner'),
            preserve_default=True,
        ),
    ]
