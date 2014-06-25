# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('hub_badge', 'name', models.CharField(max_length=50))

    def backwards(self, orm):
        db.delete_column('hub_badge', 'name')

    models = {}

    complete_apps = ['hub']
