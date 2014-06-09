# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataType'
        db.create_table(u'scraper_datatype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'scraper', ['DataType'])

        # Adding model 'ClassDef'
        db.create_table(u'scraper_classdef', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'scraper', ['ClassDef'])

        # Adding model 'FunctionDef'
        db.create_table(u'scraper_functiondef', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('klass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scraper.ClassDef'], null=True)),
            ('is_method', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('return_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['scraper.ClassDef'])),
        ))
        db.send_create_signal(u'scraper', ['FunctionDef'])

        # Adding model 'ArgDef'
        db.create_table(u'scraper_argdef', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(related_name='args', to=orm['scraper.FunctionDef'])),
            ('position', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('data_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scraper.DataType'])),
        ))
        db.send_create_signal(u'scraper', ['ArgDef'])

        # Adding model 'KwargDef'
        db.create_table(u'scraper_kwargdef', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(related_name='kwargs', to=orm['scraper.FunctionDef'])),
            ('data_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scraper.DataType'])),
        ))
        db.send_create_signal(u'scraper', ['KwargDef'])

    def backwards(self, orm):
        # Deleting model 'DataType'
        db.delete_table(u'scraper_datatype')

        # Deleting model 'ClassDef'
        db.delete_table(u'scraper_classdef')

        # Deleting model 'FunctionDef'
        db.delete_table(u'scraper_functiondef')

        # Deleting model 'ArgDef'
        db.delete_table(u'scraper_argdef')

        # Deleting model 'KwargDef'
        db.delete_table(u'scraper_kwargdef')

    models = {
        u'scraper.argdef': {
            'Meta': {'object_name': 'ArgDef'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scraper.DataType']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'args'", 'to': u"orm['scraper.FunctionDef']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'scraper.classdef': {
            'Meta': {'object_name': 'ClassDef'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'scraper.datatype': {
            'Meta': {'object_name': 'DataType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        u'scraper.functiondef': {
            'Meta': {'object_name': 'FunctionDef'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_method': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'klass': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scraper.ClassDef']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'return_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['scraper.ClassDef']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'scraper.kwargdef': {
            'Meta': {'object_name': 'KwargDef'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scraper.DataType']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'kwargs'", 'to': u"orm['scraper.FunctionDef']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['scraper']
