# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PartnerStats'
        db.create_table(u'statistics_partnerstats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('money_spent', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Partner'])),
        ))
        db.send_create_signal(u'statistics', ['PartnerStats'])


    def backwards(self, orm):
        # Deleting model 'PartnerStats'
        db.delete_table(u'statistics_partnerstats')


    models = {
        u'courses.partner': {
            'Meta': {'ordering': "('ordering',)", 'object_name': 'Partner'},
            'description': ('tinymce.models.HTMLField', [], {}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'ordering': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'statistics.partnerstats': {
            'Meta': {'object_name': 'PartnerStats'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money_spent': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Partner']"})
        }
    }

    complete_apps = ['statistics']