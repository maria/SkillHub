# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from hub.models import Account

class Migration(SchemaMigration):

    def forwards(self, orm):
        fields = (
            ('id', models.AutoField(primary_key=True)),
            ('account', models.ForeignKey(Account)),
            ('title', models.TextField()),
            ('url', models.URLField()),
            ('merged', models.DateTimeField()),
            ('repo', models.CharField(max_length=50)),
            ('repo_url', models.URLField()),
            ('created_at', models.DateTimeField()),
            ('updated_at', models.DateTimeField()),
        )

        db.create_table('hub_contribution', fields)
        db.send_create_signal('hub', ['Contribution'])

    def backwards(self, orm):
        db.drop_table('hub_contribution')

    models = {}

    complete_apps = ['hub']
