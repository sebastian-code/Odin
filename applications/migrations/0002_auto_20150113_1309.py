# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_auto_20150106_2243'),
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationSolution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApplicationTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('course', models.ForeignKey(to='courses.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='applicationsolution',
            name='task',
            field=models.ForeignKey(to='applications.ApplicationTask'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='applicationsolution',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
