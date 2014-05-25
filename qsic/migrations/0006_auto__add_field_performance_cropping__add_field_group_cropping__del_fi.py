# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Performance.cropping'
        db.add_column('qsic_performance', 'cropping',
                      self.gf('django.db.models.fields.CharField')(blank=True, default='', max_length=255),
                      keep_default=False)

        # Adding field 'Group.cropping'
        db.add_column('qsic_group', 'cropping',
                      self.gf('django.db.models.fields.CharField')(blank=True, default='', max_length=255),
                      keep_default=False)

        # Deleting field 'Performer.headshot'
        db.delete_column('qsic_performer', 'headshot')

        # Adding field 'Performer.photo'
        db.add_column('qsic_performer', 'photo',
                      self.gf('django.db.models.fields.files.ImageField')(blank=True, null=True, max_length=100),
                      keep_default=False)

        # Adding field 'Performer.cropping'
        db.add_column('qsic_performer', 'cropping',
                      self.gf('django.db.models.fields.CharField')(blank=True, default='', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Performance.cropping'
        db.delete_column('qsic_performance', 'cropping')

        # Deleting field 'Group.cropping'
        db.delete_column('qsic_group', 'cropping')

        # Adding field 'Performer.headshot'
        db.add_column('qsic_performer', 'headshot',
                      self.gf('django.db.models.fields.files.ImageField')(blank=True, null=True, max_length=100),
                      keep_default=False)

        # Deleting field 'Performer.photo'
        db.delete_column('qsic_performer', 'photo')

        # Deleting field 'Performer.cropping'
        db.delete_column('qsic_performer', 'cropping')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'qsic.event': {
            'Meta': {'object_name': 'Event', 'ordering': "['-id']"},
            '_end_dt': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            '_price': ('django.db.models.fields.DecimalField', [], {'blank': 'True', 'max_digits': '6', 'null': 'True', 'decimal_places': '2', 'default': 'None'}),
            '_start_dt': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'cropping': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '1024'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'default': "''", 'max_length': '50'})
        },
        'qsic.group': {
            'Meta': {'object_name': 'Group'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'create_dt': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'auto_now_add': 'True'}),
            'cropping': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_house_team': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'it_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'default': "''", 'max_length': '50'})
        },
        'qsic.groupperformerrelation': {
            'Meta': {'object_name': 'GroupPerformerRelation'},
            'end_dt': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qsic.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qsic.Performer']"}),
            'start_dt': ('django.db.models.fields.DateTimeField', [], {})
        },
        'qsic.performance': {
            'Meta': {'object_name': 'Performance', 'ordering': "['-end_dt']"},
            'cropping': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_dt': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['qsic.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '1024'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'blank': 'True', 'max_digits': '6', 'null': 'True', 'decimal_places': '2', 'default': 'None'}),
            'slug': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'default': "''", 'max_length': '50'}),
            'start_dt': ('django.db.models.fields.DateTimeField', [], {})
        },
        'qsic.performancegroupperformerrelation': {
            'Meta': {'object_name': 'PerformanceGroupPerformerRelation'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['qsic.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qsic.Performance']"}),
            'performer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['qsic.Performer']"})
        },
        'qsic.performer': {
            'Meta': {'object_name': 'Performer'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'cropping': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'it_id': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'it_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'default': "''", 'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['qsic']