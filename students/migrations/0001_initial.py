# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import students.validators
from django.conf import settings
import django.utils.timezone
import django.core.validators
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('courses', '0001_initial'),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], verbose_name='username', unique=True, max_length=75, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(verbose_name='first name', max_length=30, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30, blank=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=75, blank=True, unique=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('status', models.SmallIntegerField(default=1, choices=[(1, 'Student'), (2, 'HR'), (3, 'Teacher')])),
                ('avatar', django_resized.forms.ResizedImageField(upload_to='avatar', blank=True)),
                ('description', models.TextField(blank=True)),
                ('github_account', models.URLField(validators=[students.validators.validate_github], blank=True, null=True)),
                ('linkedin_account', models.URLField(validators=[students.validators.validate_linkedin], blank=True, null=True)),
                ('mac', models.CharField(validators=[students.validators.validate_mac], max_length=17, blank=True, null=True)),
                ('works_at', models.CharField(max_length='40', blank=True, null=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('mac', models.CharField(max_length=17)),
                ('date', models.DateField(auto_now=True)),
                ('student', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('cv', models.FileField(upload_to='cvs', blank=True, null=True)),
                ('group_time', models.SmallIntegerField(choices=[(1, 'Early'), (2, 'Late')])),
                ('is_attending', models.BooleanField(default=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('partner_name', models.CharField(max_length=128, blank=True, null=True)),
                ('assignment', models.ForeignKey(to='students.CourseAssignment')),
                ('partner', models.ForeignKey(to='courses.Partner', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('text', models.TextField(blank=True)),
                ('post_time', models.DateTimeField(auto_now=True)),
                ('assignment', models.ForeignKey(to='students.CourseAssignment')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
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
            field=models.ManyToManyField(to='auth.Group', blank=True, related_name='user_set', verbose_name='groups', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='hr_of',
            field=models.ForeignKey(to='courses.Partner', blank=True, null=True),
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
            field=models.ManyToManyField(to='auth.Permission', blank=True, related_name='user_set', verbose_name='user permissions', related_query_name='user', help_text='Specific permissions for this user.'),
            preserve_default=True,
        ),
    ]
