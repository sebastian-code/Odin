# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Course.image'
        db.add_column(u'courses_course', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Course.name'
        db.alter_column(u'courses_course', 'name', self.gf('django.db.models.fields.CharField')(max_length=64))

    def backwards(self, orm):
        # Deleting field 'Course.image'
        db.delete_column(u'courses_course', 'image')


        # Changing field 'Course.name'
        db.alter_column(u'courses_course', 'name', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
        u'courses.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_time': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'start_time': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['courses']