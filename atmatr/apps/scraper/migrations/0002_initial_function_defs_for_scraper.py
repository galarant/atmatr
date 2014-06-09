# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        #BASIC DATA TYPES
        dict_type = orm.DataType.objects.create(name='dict')
        list_type = orm.DataType.objects.create(name='list')
        string_type = orm.DataType.objects.create(name='string')
        int_type = orm.DataType.objects.create(name='int')
        float_type = orm.DataType.objects.create(name='float')
        boolean_type = orm.DataType.objects.create(name='boolean')
        none_type = orm.DataType.objects.create(name='None')

        #MAJOR SELENIUM CLASSES
        PhantomJS = orm.ClassDef.objects.create(name='webdriver.PhantomJS')
        WebElement = orm.ClassDef.objects.create(name='webdriver.remote.webelement.WebElement')

        #WEBDRIVER.GET
        webdriver_get = orm.FunctionDef.objects.create(name='get',
                                                       is_method=True,
                                                       klass=PhantomJS)
        orm.KwargDef.objects.create(name='url',
                                    function=webdriver_get,
                                    data_type=string_type)

        #WEBDRIVER.FIND_ELEMENT
        webdriver_find_element = orm.FunctionDef.objects.create(name='find_element',
                                                                is_method=True,
                                                                klass=PhantomJS,
                                                                return_type=WebElement)

        orm.KwargDef.objects.create(name='by',
                                    function=webdriver_find_element,
                                    data_type=string_type)

        orm.KwargDef.objects.create(name='value',
                                    function=webdriver_find_element,
                                    data_type=string_type)

        #WEBDRIVER.PAGE_SOURCE
        webdriver_page_source = orm.FunctionDef.objects.create(name='page_source',
                                                               is_method=False,
                                                               klass=PhantomJS)

        #WEBELEMENT.CLICK
        webelement_click = orm.FunctionDef.objects.create(name='click',
                                                          is_method=True,
                                                          klass=WebElement)

        #WEBELEMENT.SEND_KEYS
        webelement_send_keys = orm.FunctionDef.objects.create(name='send_keys',
                                                              is_method=True,
                                                              klass=WebElement)

        orm.ArgDef.objects.create(position=0,
                                  function=webelement_send_keys,
                                  data_type=string_type)

        #WEBELEMENT.TEXT
        webelement_text = orm.FunctionDef.objects.create(name='text',
                                                         is_method=False,
                                                         klass=WebElement)



    def backwards(self, orm):
        "Write your backwards methods here."
        data_types = orm.DataType.objects.all()
        klasses = orm.ClassDef.objects.all()
        functions = orm.FunctionDef.objects.all()

        for data_type in data_types:
            data_type.delete()

        for klass in klasses:
            klass.delete()

        for function in functions:
            function.delete()


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
    symmetrical = True
