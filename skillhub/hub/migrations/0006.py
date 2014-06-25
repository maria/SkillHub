# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from hub.models import Account, Badge


class Migration(SchemaMigration):

    def forwards(self, orm):
        fields = (
            ('id', models.AutoField(primary_key=True)),
            ('account', models.ForeignKey(Account)),
            ('badge', models.ForeignKey(Badge)),
        )

        db.create_table('hub_accountbadge', fields)
        db.send_create_signal('hub', ['AccountBadge'])

    def backwards(self, orm):
        db.drop_table('hub_accountbadge')

    models = {}

    complete_apps = ['hub']
