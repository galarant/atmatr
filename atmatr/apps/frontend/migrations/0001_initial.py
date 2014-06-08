# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PageTree'
        db.create_table(u'frontend_pagetree', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='page_trees', to=orm['auth.User'])),
            ('period', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'frontend', ['PageTree'])

        # Adding model 'ActionTree'
        db.create_table(u'frontend_actiontree', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('page_tree', self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_trees', to=orm['frontend.PageTree'])),
            ('previous_page', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='next_pages', null=True, to=orm['frontend.ActionTree'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=2048)),
        ))
        db.send_create_signal(u'frontend', ['ActionTree'])

        # Adding model 'Action'
        db.create_table(u'frontend_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('action_tree', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', to=orm['frontend.ActionTree'])),
            ('previous_action', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='next_actions', null=True, to=orm['frontend.Action'])),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scraper.FunctionDef'])),
        ))
        db.send_create_signal(u'frontend', ['Action'])

        # Adding model 'ActionArg'
        db.create_table(u'frontend_actionarg', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='args', to=orm['frontend.Action'])),
            ('arg_def', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['scraper.ArgDef'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=2048)),
        ))
        db.send_create_signal(u'frontend', ['ActionArg'])

        # Adding model 'ActionKwarg'
        db.create_table(u'frontend_actionkwarg', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='kwargs', to=orm['frontend.Action'])),
            ('arg_def', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['scraper.KwargDef'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=2048)),
        ))
        db.send_create_signal(u'frontend', ['ActionKwarg'])

    def backwards(self, orm):
        # Deleting model 'PageTree'
        db.delete_table(u'frontend_pagetree')

        # Deleting model 'ActionTree'
        db.delete_table(u'frontend_actiontree')

        # Deleting model 'Action'
        db.delete_table(u'frontend_action')

        # Deleting model 'ActionArg'
        db.delete_table(u'frontend_actionarg')

        # Deleting model 'ActionKwarg'
        db.delete_table(u'frontend_actionkwarg')

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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'frontend.action': {
            'Meta': {'object_name': 'Action'},
            'action_tree': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': u"orm['frontend.ActionTree']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scraper.FunctionDef']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'previous_action': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'next_actions'", 'null': 'True', 'to': u"orm['frontend.Action']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'frontend.actionarg': {
            'Meta': {'object_name': 'ActionArg'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'args'", 'to': u"orm['frontend.Action']"}),
            'arg_def': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['scraper.ArgDef']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        },
        u'frontend.actionkwarg': {
            'Meta': {'object_name': 'ActionKwarg'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'kwargs'", 'to': u"orm['frontend.Action']"}),
            'arg_def': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['scraper.KwargDef']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        },
        u'frontend.actiontree': {
            'Meta': {'object_name': 'ActionTree'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'page_tree': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'action_trees'", 'to': u"orm['frontend.PageTree']"}),
            'previous_page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'next_pages'", 'null': 'True', 'to': u"orm['frontend.ActionTree']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2048'})
        },
        u'frontend.pagetree': {
            'Meta': {'object_name': 'PageTree'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'period': ('django.db.models.fields.FloatField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'page_trees'", 'to': u"orm['auth.User']"})
        },
        u'scraper.argdef': {
            'Meta': {'object_name': 'ArgDef'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
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
        u'scraper.functiondef': {
            'Meta': {'object_name': 'FunctionDef'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scraper.ClassDef']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'scraper.kwargdef': {
            'Meta': {'object_name': 'KwargDef'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'kwargs'", 'to': u"orm['scraper.FunctionDef']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['frontend']