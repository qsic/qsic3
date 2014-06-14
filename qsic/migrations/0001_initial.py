# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QSICPic'
        db.create_table('qsic_qsicpic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True, null=True)),
            ('banner_crop', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['qsic.Event'])),
            ('performance', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['qsic.Performance'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['qsic.Group'])),
            ('performer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['qsic.Performer'])),
        ))
        db.send_create_signal('qsic', ['QSICPic'])

        # Adding model 'Performer'
        db.create_table('qsic_performer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, unique=True, null=True, to=orm['auth.User'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=50, blank=True)),
            ('it_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True, null=True)),
            ('it_id', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True, null=True)),
            ('detail_crop', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('qsic', ['Performer'])

        # Adding model 'Group'
        db.create_table('qsic_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=50, blank=True)),
            ('it_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True, null=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True, null=True)),
            ('detail_crop', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('banner_crop', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
            ('create_dt', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True, null=True)),
            ('is_house_team', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('qsic', ['Group'])

        # Adding model 'GroupPerformerRelation'
        db.create_table('qsic_groupperformerrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qsic.Group'])),
            ('performer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qsic.Performer'])),
            ('start_dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_dt', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
        ))
        db.send_create_signal('qsic', ['GroupPerformerRelation'])

        # Adding model 'Event'
        db.create_table('qsic_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=50, blank=True)),
            ('_start_dt', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
            ('_end_dt', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
            ('_price', self.gf('django.db.models.fields.DecimalField')(default=None, blank=True, max_digits=6, decimal_places=2, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True, null=True)),
            ('detail_crop', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('banner_crop', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('qsic', ['Event'])

        # Adding model 'Performance'
        db.create_table('qsic_performance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['qsic.Event'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=50, blank=True)),
            ('start_dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=None, blank=True, max_digits=6, decimal_places=2, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True, null=True)),
            ('detail_crop', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('banner_crop', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('qsic', ['Performance'])

        # Adding model 'PerformanceGroupPerformerRelation'
        db.create_table('qsic_performancegroupperformerrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('performance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qsic.Performance'])),
            ('performer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['qsic.Performer'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['qsic.Group'])),
        ))
        db.send_create_signal('qsic', ['PerformanceGroupPerformerRelation'])


    def backwards(self, orm):
        # Deleting model 'QSICPic'
        db.delete_table('qsic_qsicpic')

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
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'qsic.event': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Event'},
            '_end_dt': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            '_price': ('django.db.models.fields.DecimalField', [], {'default': 'None', 'blank': 'True', 'max_digits': '6', 'decimal_places': '2', 'null': 'True'}),
            '_start_dt': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'banner_crop': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'detail_crop': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50', 'blank': 'True'})
        },
        'qsic.group': {
            'Meta': {'object_name': 'Group'},
            'banner_crop': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'create_dt': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True', 'null': 'True'}),
            'detail_crop': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_house_team': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'it_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50', 'blank': 'True'})
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
            'Meta': {'ordering': "['-end_dt']", 'object_name': 'Performance'},
            'banner_crop': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'detail_crop': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'end_dt': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['qsic.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': 'None', 'blank': 'True', 'max_digits': '6', 'decimal_places': '2', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
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
            'detail_crop': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'it_id': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'it_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'qsic.qsicpic': {
            'Meta': {'object_name': 'QSICPic'},
            'banner_crop': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['qsic.Event']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['qsic.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performance': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['qsic.Performance']"}),
            'performer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['qsic.Performer']"}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['qsic']