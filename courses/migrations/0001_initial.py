# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('issues_closed', models.IntegerField(default=0)),
                ('issues_opened', models.IntegerField(default=0)),
                ('total_commits', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', tinymce.models.HTMLField()),
                ('git_repository', models.CharField(max_length=256, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'courses_logoes', blank=True)),
                ('name', models.CharField(max_length=64)),
                ('short_description', models.CharField(max_length=300, blank=True)),
                ('show_on_index', models.BooleanField(default=False)),
                ('is_free', models.BooleanField(default=True)),
                ('application_until', models.DateField()),
                ('applications_url', models.URLField(null=True, blank=True)),
                ('ask_for_favorite_partner', models.BooleanField(default=False)),
                ('ask_for_feedback', models.BooleanField(default=False)),
                ('end_time', models.DateField(null=True, blank=True)),
                ('next_season_mail_list', models.URLField(null=True, blank=True)),
                ('SEO_description', models.CharField(max_length=255)),
                ('SEO_title', models.CharField(max_length=255)),
                ('start_time', models.DateField(null=True, blank=True)),
                ('url', models.SlugField(unique=True, max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', tinymce.models.HTMLField()),
                ('facebook', models.URLField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('logo', models.ImageField(null=True, upload_to=b'partner_logoes', blank=True)),
                ('money_spent', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=128)),
                ('ordering', models.PositiveSmallIntegerField(default=0)),
                ('twitter', models.URLField(null=True, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
            ],
            options={
                'ordering': ('ordering',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deadline', models.DateTimeField(null=True, blank=True)),
                ('description', models.URLField()),
                ('is_exam', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=128)),
                ('week', models.CharField(max_length=10)),
                ('course', models.ForeignKey(to='courses.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WeeklyCommit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('commits_count', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('name', 'description')]),
        ),
        migrations.AddField(
            model_name='course',
            name='partner',
            field=models.ManyToManyField(to='courses.Partner', null=True, blank=True),
            preserve_default=True,
        ),
    ]
