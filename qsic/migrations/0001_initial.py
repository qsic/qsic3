# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Performer'
        db.create_table('qsic_performer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(null=True, unique=True, to=orm['auth.User'], blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('it_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('it_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('headshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('qsic', ['Performer'])

        # Adding model 'Group'
        db.create_table('qsic_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('it_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('create_dt', self.gf('django.db.models.fields.DateTimeField')(null=True, auto_now_add=True, blank=True)),
            ('is_house_team', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('qsic', ['Group'])

        # Adding model 'GroupPerformerRelation'
        db.create_table('qsic_groupperformerrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qsic.Group'])),
            ('performer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qsic.Performer'])),
            ('start_dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_dt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('qsic', ['GroupPerformerRelation'])

        # Adding model 'Event'
        db.create_table('qsic_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True)),
            ('_start_dt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('_end_dt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('_price', self.gf('django.db.models.fields.DecimalField')(default=None, max_digits=6, decimal_places=2, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('qsic', ['Event'])

        # Adding model 'Performance'
        db.create_table('qsic_performance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['qsic.Event'], blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True)),
            ('start_dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=None, max_digits=6, decimal_places=2, null=True, blank=True)),
        ))
        db.send_create_signal('qsic', ['Performance'])

        # Adding model 'PerformanceGroupPerformerRelation'
        db.create_table('qsic_performancegroupperformerrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('performance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qsic.Performance'])),
            ('performer', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['qsic.Performer'], blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['qsic.Group'], blank=True)),
        ))
        db.send_create_signal('qsic', ['PerformanceGroupPerformerRelation'])


    def backwards(self, orm):
        # Deleting model 'Performer'
        db.delete_table('qsic_performer')

        # Deleting model 'Group'
        db.delete_table('qsic_group')

        # Deleting model 'GroupPerformerRelation'
        db.delete_table('qsic_groupperformerrelation')

        # Deleting model 'Event'
        db.delete_table('qsic_event')

        # Deleting model 'Performance'
        db.delete_table('qsic_performance')

        # Deleting model 'PerformanceGroupPerformerRelation'
        db.delete_table('qsic_performancegroupperformerrelation')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'qsic.event': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Event'},
            '_end_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            '_price': ('django.db.models.fields.DecimalField', [], {'default': 'None', 'max_digits': '6', 'decimal_places': '2', 'null': 'True', 'blank': 'True'}),
            '_start_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'})
        },
        'qsic.group': {
            'Meta': {'object_name': 'Group'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'create_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_house_team': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'it_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'qsic.groupperformerrelation': {
            'Meta': {'object_name': 'GroupPerformerRelation'},
            'end_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qsic.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qsic.Performer']"}),
            'start_dt': ('django.db.models.fields.DateTimeField', [], {})
        },
        'qsic.performance': {
            'Meta': {'ordering': "['-end_dt']", 'object_name': 'Performance'},
            'end_dt': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['qsic.Event']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': 'None', 'max_digits': '6', 'decimal_places': '2', 'null': 'True', 'blank': 'True'}),
            'start_dt': ('django.db.models.fields.DateTimeField', [], {})
        },
        'qsic.performancegroupperformerrelation': {
            'Meta': {'object_name': 'PerformanceGroupPerformerRelation'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['qsic.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qsic.Performance']"}),
            'performer': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['qsic.Performer']", 'blank': 'True'})
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
            'user': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'unique': 'True', 'to': "orm['auth.User']", 'blank': 'True'})
        }
    }

    complete_apps = ['qsic']