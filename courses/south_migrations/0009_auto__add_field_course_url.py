# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Course.url'
        db.add_column(u'courses_course', 'url',
                      self.gf('django.db.models.fields.SlugField')(default='', unique=True, max_length=80),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Course.url'
        db.delete_column(u'courses_course', 'url')


    models = {
        u'courses.course': {
            'Meta': {'object_name': 'Course'},
            'SEO_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SEO_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'applications_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'enable_applications': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_time': ('django.db.models.fields.DateField', [], {}),
            'git_repository': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'show_on_index': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start_time': ('django.db.models.fields.DateField', [], {}),
            'url': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '80'})
        }
    }

    complete_apps = ['courses']