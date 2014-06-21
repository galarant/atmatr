# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        """
        Adds models for the basic tags defined in:
        http://www.webmonkey.com/2010/02/html_cheatsheet/
        """

        # BASIC TAGS
        orm.Tag.objects.create(name='html', show_content=False)
        orm.Tag.objects.create(name='head', show_content=False)
        orm.Tag.objects.create(name='body', show_content=False)
        orm.Tag.objects.create(name='frame', show_content=False)

        # TEXT TAGS
        orm.Tag.objects.create(name='h1')
        orm.Tag.objects.create(name='h2')
        orm.Tag.objects.create(name='h3')
        orm.Tag.objects.create(name='h4')
        orm.Tag.objects.create(name='h5')
        orm.Tag.objects.create(name='h6')
        orm.Tag.objects.create(name='b')
        orm.Tag.objects.create(name='i')
        orm.Tag.objects.create(name='u')
        orm.Tag.objects.create(name='tt')
        orm.Tag.objects.create(name='pre')
        orm.Tag.objects.create(name='cite')
        orm.Tag.objects.create(name='em')
        orm.Tag.objects.create(name='strong')
        orm.Tag.objects.create(name='font')
        orm.Tag.objects.create(name='strike')
        orm.Tag.objects.create(name='sup')
        orm.Tag.objects.create(name='sub')

        # LINK TAG
        orm.Tag.objects.create(name='a')

        # FORMATTING TAGS
        orm.Tag.objects.create(name='p')
        orm.Tag.objects.create(name='blockquote')
        orm.Tag.objects.create(name='dl')
        orm.Tag.objects.create(name='dt')
        orm.Tag.objects.create(name='dd')
        orm.Tag.objects.create(name='ol')
        orm.Tag.objects.create(name='ul')
        orm.Tag.objects.create(name='li')
        orm.Tag.objects.create(name='div')
        orm.Tag.objects.create(name='img')

        # TABLE TAGS
        orm.Tag.objects.create(name='table')
        orm.Tag.objects.create(name='th')
        orm.Tag.objects.create(name='tr')
        orm.Tag.objects.create(name='td')

        # FORM TAGS
        orm.Tag.objects.create(name='form')
        orm.Tag.objects.create(name='select')
        orm.Tag.objects.create(name='option')
        orm.Tag.objects.create(name='textarea')
        orm.Tag.objects.create(name='input')
        orm.Tag.objects.create(name='button')
        orm.Tag.objects.create(name='label')

    def backwards(self, orm):
        all_tags = orm.Tag.objects.all()
        for tag in all_tags:
            tag.delete()

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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scraper.FunctionDef']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['frontend.Page']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['frontend.Action']"}),
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
        u'frontend.page': {
            'Meta': {'object_name': 'Page'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['frontend.Page']"}),
            'script': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['frontend.Script']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2048'})
        },
        u'frontend.script': {
            'Meta': {'object_name': 'Script'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'period': ('django.db.models.fields.FloatField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'frontend.tag': {
            'Meta': {'object_name': 'Tag'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'show_content': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
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

    complete_apps = ['frontend']
    symmetrical = True