# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        fields = (
            ('id', models.AutoField(primary_key=True)),
            ('type', models.CharField(max_length=50)),
            ('url', models.URLField()),
        )

        db.create_table('hub_badge', fields)
        db.send_create_signal('hub', ['Badge'])

    def backwards(self, orm):
        db.drop_table('hub_badge')

    models = {}

    complete_apps = ['hub']
