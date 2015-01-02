# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms
import students.validators
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('forum', '__first__'),
        ('courses', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=75, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(unique=True, max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('status', models.SmallIntegerField(default=1, choices=[(1, 'Student'), (2, 'HR'), (3, 'Teacher')])),
                ('avatar', django_resized.forms.ResizedImageField(upload_to='avatar', blank=True)),
                ('description', models.TextField(blank=True)),
                ('github_account', models.URLField(blank=True, null=True, validators=[students.validators.validate_github])),
                ('linkedin_account', models.URLField(blank=True, null=True, validators=[students.validators.validate_linkedin])),
                ('mac', models.CharField(blank=True, max_length=17, null=True, validators=[students.validators.validate_mac])),
                ('works_at', models.CharField(max_length='40', null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mac', models.CharField(max_length=17)),
                ('date', models.DateField(auto_now=True)),
                ('student', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cv', models.FileField(null=True, upload_to='cvs', blank=True)),
                ('group_time', models.SmallIntegerField(choices=[(1, 'Early'), (2, 'Late')])),
                ('points', models.PositiveIntegerField(default=0)),
                ('course', models.ForeignKey(to='courses.Course')),
                ('favourite_partners', models.ManyToManyField(to='courses.Partner')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HrLoginLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('repo', models.URLField()),
                ('task', models.ForeignKey(to='courses.Task')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudentStartedWorkingAt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('partner_name', models.CharField(max_length=128, null=True, blank=True)),
                ('assignment', models.ForeignKey(to='students.CourseAssignment')),
                ('partner', models.ForeignKey(blank=True, to='courses.Partner', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(blank=True)),
                ('post_time', models.DateTimeField(auto_now=True)),
                ('assignment', models.ForeignKey(to='students.CourseAssignment')),
                ('author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='solution',
            unique_together=set([('user', 'task')]),
        ),
        migrations.AlterUniqueTogether(
            name='courseassignment',
            unique_together=set([('user', 'course')]),
        ),
        migrations.AlterUniqueTogether(
            name='checkin',
            unique_together=set([('student', 'date')]),
        ),
        migrations.AddField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(to='courses.Course', through='students.CourseAssignment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='hr_of',
            field=models.ForeignKey(blank=True, to='courses.Partner', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='subscribed_topics',
            field=models.ManyToManyField(to='forum.Topic', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
