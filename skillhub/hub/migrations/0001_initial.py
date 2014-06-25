# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from south.db import db
from south.v2 import SchemaMigration

from hub.models import Account, Project

class Migration(SchemaMigration):


    def forwards(self, orm):
        fields = (
            ('id', models.AutoField(primary_key=True)),
            ('user', models.OneToOneField(User)),
            ('github_url', models.URLField()),
            ('github_token', models.TextField()),
            ('avatar_url', models.TextField()),
        )
        db.create_table('hub_account', fields)
        db.send_create_signal('hub', ['Account'])

        fields = (
            ('id', models.AutoField(primary_key=True)),
            ('account', models.ForeignKey(Account)),
            ('type', models.CharField(max_length=30)),
            ('name', models.CharField(max_length=50)),
            ('url', models.URLField(null=True, blank=True)),
            ('description', models.TextField()),
            ('stars', models.IntegerField()),
            ('forks', models.IntegerField()),
        )
        db.create_table('hub_project', fields)
        db.send_create_signal('hub', ['Project'])

        fields = (
            ('id', models.AutoField(primary_key=True)),
            ('project', models.ForeignKey(Project)),
            ('name', models.CharField(max_length=50)),
            ('percentage', models.FloatField()),
        )
        db.create_table('hub_language', fields)
        db.send_create_signal('hub', ['Language'])

        fields = (
            ('id', models.AutoField(primary_key=True)),
            ('account', models.ForeignKey(Account)),
            ('name', models.CharField(max_length=50)),
            ('level', models.FloatField()),
        )
        db.create_table('hub_skill', fields)
        db.send_create_signal('hub', ['Skill'])

        fields = (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=50)),
            ('description', models.TextField()),
        )
        db.create_table('hub_tip', fields)
        db.send_create_signal('hub', ['Tip'])


        fields = (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=50)),
            ('description', models.TextField()),
            ('url', models.URLField(null=True, blank=True)),
        )
        db.create_table('hub_tutorial', fields)
        db.send_create_signal('hub', ['Tutorial'])

    def backwards(self, orm):
        db.delete_table('hub_account')
        db.delete_table('hub_project')
        db.delete_table('hub_tip')
        db.delete_table('hub_tutorial')
        db.delete_table('hub_skill')
        db.delete_table('hub_language')

    models = {}

    complete_apps = ['hub']
