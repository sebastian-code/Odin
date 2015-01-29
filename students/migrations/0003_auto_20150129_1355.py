# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import students.validators


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_courseassignment_is_online'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationInstitution',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='usernote',
            options={'ordering': ('post_time',)},
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
            field=models.ManyToManyField(blank=True, null=True, to='courses.Partner'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solution',
            name='repo',
            field=models.URLField(validators=[students.validators.validate_github]),
            preserve_default=True,
        ),
    ]
