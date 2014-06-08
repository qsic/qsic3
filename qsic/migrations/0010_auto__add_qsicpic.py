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
            ('description', self.gf('django.db.models.fields.CharField')(blank=True, max_length=256)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(null=True, blank=True, max_length=100)),
            ('banner_crop', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['qsic.Event'])),
            ('performance', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['qsic.Performance'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['qsic.Group'])),
            ('performer', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['qsic.Performer'])),
        ))
        db.send_create_signal('qsic', ['QSICPic'])


    def backwards(self, orm):
        # Deleting model 'QSICPic'
        db.delete_table('qsic_qsicpic')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
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
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"}),
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
            '_end_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            '_price': ('django.db.models.fields.DecimalField', [], {'default': 'None', 'null': 'True', 'decimal_places': '2', 'blank': 'True', 'max_digits': '6'}),
            '_start_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'banner_crop': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'detail_crop': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'blank': 'True', 'max_length': '1024'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'blank': 'True', 'max_length': '50'})
        },
        'qsic.group': {
            'Meta': {'object_name': 'Group'},
            'banner_crop': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'create_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'detail_crop': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_house_team': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'it_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'blank': 'True', 'max_length': '50'})
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
            'banner_crop': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'detail_crop': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'end_dt': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['qsic.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'blank': 'True', 'max_length': '1024'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': 'None', 'null': 'True', 'decimal_places': '2', 'blank': 'True', 'max_digits': '6'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'blank': 'True', 'max_length': '50'}),
            'start_dt': ('django.db.models.fields.DateTimeField', [], {})
        },
        'qsic.performancegroupperformerrelation': {
            'Meta': {'object_name': 'PerformanceGroupPerformerRelation'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['qsic.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qsic.Performance']"}),
            'performer': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['qsic.Performer']"})
        },
        'qsic.performer': {
            'Meta': {'object_name': 'Performer'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'detail_crop': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'it_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'it_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'blank': 'True', 'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'to': "orm['auth.User']", 'blank': 'True', 'unique': 'True'})
        },
        'qsic.qsicpic': {
            'Meta': {'object_name': 'QSICPic'},
            'banner_crop': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '256'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['qsic.Event']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['qsic.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performance': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['qsic.Performance']"}),
            'performer': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['qsic.Performer']"}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['qsic']