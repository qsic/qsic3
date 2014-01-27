# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Group.create_dt'
        db.add_column('qsic_group', 'create_dt',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 26, 0, 0), blank=True, auto_now_add=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Group.create_dt'
        db.delete_column('qsic_group', 'create_dt')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'qsic.event': {
            'Meta': {'object_name': 'Event', 'ordering': "['-id']"},
            '_end_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            '_price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'default': 'None', 'max_digits': '6', 'null': 'True', 'blank': 'True'}),
            '_start_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qsic.EventSeries']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'default': "''", 'blank': 'True'})
        },
        'qsic.eventseries': {
            'Meta': {'object_name': 'EventSeries', 'ordering': "['-id']"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'default': "''", 'blank': 'True'})
        },
        'qsic.group': {
            'Meta': {'object_name': 'Group'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'create_dt': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'it_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'qsic.groupperformerrelation': {
            'Meta': {'object_name': 'GroupPerformerRelation'},
            'end_dt': ('django.db.models.fields.DateTimeField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qsic.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qsic.Performer']"}),
            'start_dt': ('django.db.models.fields.DateTimeField', [], {})
        },
        'qsic.performance': {
            'Meta': {'object_name': 'Performance', 'ordering': "['-end_dt']"},
            'end_dt': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qsic.Event']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'default': "''", 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'default': 'None', 'max_digits': '6', 'null': 'True', 'blank': 'True'}),
            'start_dt': ('django.db.models.fields.DateTimeField', [], {})
        },
        'qsic.performancegroupperformerrelation': {
            'Meta': {'object_name': 'PerformanceGroupPerformerRelation'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qsic.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qsic.Performance']"}),
            'performer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qsic.Performer']", 'null': 'True', 'blank': 'True'})
        },
        'qsic.performer': {
            'Meta': {'object_name': 'Performer'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'headshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'it_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'it_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['qsic']