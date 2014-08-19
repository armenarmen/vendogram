# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Profile.email'
        db.add_column(u'main_app_profile', 'email',
                      self.gf('django.db.models.fields.EmailField')(default='armenlsuny@gmail.com', max_length=75),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Profile.email'
        db.delete_column(u'main_app_profile', 'email')


    models = {
        u'main_app.profile': {
            'Meta': {'object_name': 'Profile'},
            'access_token': ('django.db.models.fields.TextField', [], {}),
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '2200', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagram_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'profile_picture': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['main_app']