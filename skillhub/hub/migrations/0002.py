# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('hub_account', 'created_at',
                      models.DateTimeField(auto_now_add=True, null=True, blank=True))
        db.add_column('hub_account', 'updated_at',
                      models.DateTimeField(auto_now_add=True, null=True, blank=True))
        db.add_column('hub_project', 'created_at',
                      models.DateTimeField(auto_now_add=True, null=True, blank=True))
        db.add_column('hub_project', 'updated_at',
                      models.DateTimeField(auto_now_add=True, null=True, blank=True))

    def backwards(self, orm):
        db.delete_column('hub_account', 'created_at')
        db.delete_column('hub_account', 'updated_at')
        db.delete_column('hub_project', 'created_at')
        db.delete_column('hub_project', 'updated_at')

    models = {}

    complete_apps = ['hub']
