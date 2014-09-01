# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'User.linkedin_account'
        db.alter_column(u'students_user', 'linkedin_account', self.gf('django.db.models.fields.URLField')(default='', max_length=200))

        # Changing field 'User.mac'
        db.alter_column(u'students_user', 'mac', self.gf('django.db.models.fields.CharField')(default='', max_length=17))

        # Changing field 'User.works_at'
        db.alter_column(u'students_user', 'works_at', self.gf('django.db.models.fields.CharField')(default='', max_length='40'))

        # Changing field 'User.github_account'
        db.alter_column(u'students_user', 'github_account', self.gf('django.db.models.fields.URLField')(default='', max_length=200))

        # Changing field 'CourseAssignment.cv'
        db.alter_column(u'students_courseassignment', 'cv', self.gf('django.db.models.fields.files.FileField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'User.linkedin_account'
        db.alter_column(u'students_user', 'linkedin_account', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

        # Changing field 'User.mac'
        db.alter_column(u'students_user', 'mac', self.gf('django.db.models.fields.CharField')(max_length=17, null=True))

        # Changing field 'User.works_at'
        db.alter_column(u'students_user', 'works_at', self.gf('django.db.models.fields.CharField')(max_length='40', null=True))

        # Changing field 'User.github_account'
        db.alter_column(u'students_user', 'github_account', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

        # Changing field 'CourseAssignment.cv'
        db.alter_column(u'students_courseassignment', 'cv', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'courses.course': {
            'Meta': {'object_name': 'Course'},
            'SEO_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SEO_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'application_until': ('django.db.models.fields.DateField', [], {}),
            'applications_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'ask_for_favorite_partner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ask_for_feedback': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('tinymce.models.HTMLField', [], {}),
            'end_time': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'git_repository': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'next_season_mail_list': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['courses.Partner']", 'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'show_on_index': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start_time': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '80'})
        },
        u'courses.partner': {
            'Meta': {'ordering': "('ordering',)", 'object_name': 'Partner'},
            'description': ('tinymce.models.HTMLField', [], {}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'ordering': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'courses.task': {
            'Meta': {'unique_together': "(('name', 'description'),)", 'object_name': 'Task'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Course']"}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_exam': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'week': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'forum.category': {
            'Meta': {'ordering': "('ordering',)", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'forum.topic': {
            'Meta': {'object_name': 'Topic'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['students.User']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['forum.Category']"}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'students.checkin': {
            'Meta': {'unique_together': "(('student', 'date'),)", 'object_name': 'CheckIn'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['students.User']", 'null': 'True', 'blank': 'True'})
        },
        u'students.courseassignment': {
            'Meta': {'unique_together': "(('user', 'course'),)", 'object_name': 'CourseAssignment'},
            'after_course_works_at': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'after_course_works'", 'null': 'True', 'to': u"orm['courses.Partner']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Course']"}),
            'cv': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'favourite_partners': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['courses.Partner']", 'symmetrical': 'False'}),
            'group_time': ('django.db.models.fields.SmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['students.User']"})
        },
        u'students.hrloginlog': {
            'Meta': {'object_name': 'HrLoginLog'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['students.User']"})
        },
        u'students.solution': {
            'Meta': {'unique_together': "(('user', 'task'),)", 'object_name': 'Solution'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['students.User']"})
        },
        u'students.user': {
            'Meta': {'object_name': 'User'},
            'avatar': ('django_resized.forms.ResizedImageField', [], {'max_length': '100', 'max_width': '200', 'blank': 'True'}),
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['courses.Course']", 'through': u"orm['students.CourseAssignment']", 'symmetrical': 'False'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'github_account': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'hr_of': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Partner']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'linkedin_account': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '17', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'subscribed_topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['forum.Topic']", 'symmetrical': 'False', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'}),
            'works_at': ('django.db.models.fields.CharField', [], {'max_length': "'40'", 'blank': 'True'})
        },
        u'students.usernote': {
            'Meta': {'object_name': 'UserNote'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['students.CourseAssignment']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['students.User']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['students']