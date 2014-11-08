# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Course.end_time'
        db.delete_column(u'courses_course', 'end_time')

        # Deleting field 'Course.start_time'
        db.delete_column(u'courses_course', 'start_time')

        # Deleting field 'Course.enable_applications'
        db.delete_column(u'courses_course', 'enable_applications')

        # Adding field 'Course.application_until'
        db.add_column(u'courses_course', 'application_until',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 4, 19, 0, 0)),
                      keep_default=False)

        # Adding field 'Course.next_season_mail_list'
        db.add_column(u'courses_course', 'next_season_mail_list',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


        # Changing field 'Course.description'
        db.alter_column(u'courses_course', 'description', self.gf('tinymce.models.HTMLField')())

    def backwards(self, orm):
        # Adding field 'Course.end_time'
        db.add_column(u'courses_course', 'end_time',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 4, 19, 0, 0)),
                      keep_default=False)

        # Adding field 'Course.start_time'
        db.add_column(u'courses_course', 'start_time',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 4, 19, 0, 0)),
                      keep_default=False)

        # Adding field 'Course.enable_applications'
        db.add_column(u'courses_course', 'enable_applications',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Course.application_until'
        db.delete_column(u'courses_course', 'application_until')

        # Deleting field 'Course.next_season_mail_list'
        db.delete_column(u'courses_course', 'next_season_mail_list')


        # Changing field 'Course.description'
        db.alter_column(u'courses_course', 'description', self.gf('django.db.models.fields.TextField')())

    models = {
        u'courses.course': {
            'Meta': {'object_name': 'Course'},
            'SEO_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SEO_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'application_until': ('django.db.models.fields.DateField', [], {}),
            'applications_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'description': ('tinymce.models.HTMLField', [], {}),
            'git_repository': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'next_season_mail_list': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'show_on_index': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '80'})
        }
    }

    complete_apps = ['courses']
