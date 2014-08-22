# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StripeKey'
        db.create_table(u'main_app_stripekey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stripe_key_profile', to=orm['main_app.Profile'])),
            ('stripe_key', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'main_app', ['StripeKey'])


    def backwards(self, orm):
        # Deleting model 'StripeKey'
        db.delete_table(u'main_app_stripekey')


    models = {
        u'main_app.profile': {
            'Meta': {'object_name': 'Profile'},
            'access_token': ('django.db.models.fields.TextField', [], {}),
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '2200', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "'armenlsuny@gmail.com'", 'max_length': '75'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagram_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'profile_picture': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'main_app.stripekey': {
            'Meta': {'object_name': 'StripeKey'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stripe_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stripe_key_profile'", 'to': u"orm['main_app.Profile']"})
        }
    }

    complete_apps = ['main_app']