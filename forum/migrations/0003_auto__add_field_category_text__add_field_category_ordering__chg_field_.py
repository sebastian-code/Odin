# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Category.text'
        db.add_column(u'forum_category', 'text',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=512),
                      keep_default=False)

        # Adding field 'Category.ordering'
        db.add_column(u'forum_category', 'ordering',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0),
                      keep_default=False)


        # Changing field 'Category.title'
        db.alter_column(u'forum_category', 'title', self.gf('django.db.models.fields.CharField')(max_length=128))

    def backwards(self, orm):
        # Deleting field 'Category.text'
        db.delete_column(u'forum_category', 'text')

        # Deleting field 'Category.ordering'
        db.delete_column(u'forum_category', 'ordering')


        # Changing field 'Category.title'
        db.alter_column(u'forum_category', 'title', self.gf('django.db.models.fields.CharField')(max_length=512))

    models = {
        u'forum.category': {
            'Meta': {'ordering': "('ordering',)", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['forum']