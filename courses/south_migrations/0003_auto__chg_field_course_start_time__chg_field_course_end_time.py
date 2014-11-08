# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Course.start_time'
        db.alter_column(u'courses_course', 'start_time', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Course.end_time'
        db.alter_column(u'courses_course', 'end_time', self.gf('django.db.models.fields.DateField')())

    def backwards(self, orm):

        # Changing field 'Course.start_time'
        db.alter_column(u'courses_course', 'start_time', self.gf('django.db.models.fields.TimeField')())

        # Changing field 'Course.end_time'
        db.alter_column(u'courses_course', 'end_time', self.gf('django.db.models.fields.TimeField')())

    models = {
        u'courses.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_time': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'start_time': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['courses']