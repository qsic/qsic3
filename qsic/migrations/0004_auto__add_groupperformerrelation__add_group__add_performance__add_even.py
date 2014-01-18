# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GroupPerformerRelation'
        db.create_table('qsic_groupperformerrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qsic.Group'])),
            ('performer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qsic.Performer'])),
            ('start_dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_dt', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('qsic', ['GroupPerformerRelation'])

        # Adding model 'Group'
        db.create_table('qsic_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('it_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True, null=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True, null=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
        ))
        db.send_create_signal('qsic', ['Group'])

        # Adding model 'Performance'
        db.create_table('qsic_performance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['qsic.Event'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024, default='', blank=True)),
            ('start_dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, blank=True, max_digits=6)),
        ))
        db.send_create_signal('qsic', ['Performance'])

        # Adding model 'Event'
        db.create_table('qsic_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_series', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['qsic.EventSeries'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024, default='', blank=True)),
            ('start_dt', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('end_dt', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, blank=True, max_digits=6)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('qsic', ['Event'])

        # Adding model 'PerformanceGroupPerformerRelation'
        db.create_table('qsic_performancegroupperformerrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('performance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qsic.Performance'])),
            ('performer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['qsic.Performer'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['qsic.Group'])),
        ))
        db.send_create_signal('qsic', ['PerformanceGroupPerformerRelation'])

        # Adding model 'EventSeries'
        db.create_table('qsic_eventseries', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024, default='', blank=True)),
            ('start_dt', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('end_dt', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, blank=True, max_digits=6)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('qsic', ['EventSeries'])


    def backwards(self, orm):
        # Deleting model 'GroupPerformerRelation'
        db.delete_table('qsic_groupperformerrelation')

        # Deleting model 'Group'
        db.delete_table('qsic_group')

        # Deleting model 'Performance'
        db.delete_table('qsic_performance')

        # Deleting model 'Event'
        db.delete_table('qsic_event')

        # Deleting model 'PerformanceGroupPerformerRelation'
        db.delete_table('qsic_performancegroupperformerrelation')

        # Deleting model 'EventSeries'
        db.delete_table('qsic_eventseries')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']", 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'qsic.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_dt': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'event_series': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['qsic.EventSeries']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'default': "''", 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'blank': 'True', 'max_digits': '6'}),
            'start_dt': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        'qsic.eventseries': {
            'Meta': {'object_name': 'EventSeries', 'ordering': "['-end_dt']"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_dt': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'default': "''", 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'blank': 'True', 'max_digits': '6'}),
            'start_dt': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        'qsic.group': {
            'Meta': {'object_name': 'Group'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'it_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'})
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
            'Meta': {'object_name': 'Performance'},
            'end_dt': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['qsic.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'default': "''", 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'blank': 'True', 'max_digits': '6'}),
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
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'headshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'it_id': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'it_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'blank': 'True', 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['qsic']