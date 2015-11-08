# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text=b'When this instance was created', auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(help_text=b'When this instance was last updated', auto_now=True, null=True)),
                ('github_url', models.URLField()),
                ('github_token', models.TextField()),
                ('avatar_url', models.TextField()),
                ('synced_at', models.DateTimeField(null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AccountBadge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.ForeignKey(to='hub.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50, choices=[(b'TEN_CONTRIBUTIONS', b'ten_contrib'), (b'FIRST_CONTRIBUTION', b'first_contrib'), (b'FIVE_SKILLS', b'five_skills')])),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text=b'When this instance was created', auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(help_text=b'When this instance was last updated', auto_now=True, null=True)),
                ('title', models.TextField()),
                ('url', models.URLField()),
                ('merged', models.DateTimeField()),
                ('repo', models.CharField(max_length=50)),
                ('repo_url', models.URLField()),
                ('account', models.ForeignKey(to='hub.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('percentage', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text=b'When this instance was created', auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(help_text=b'When this instance was last updated', auto_now=True, null=True)),
                ('type', models.CharField(max_length=30, choices=[(b'PRACTICE', b'Practice'), (b'LEARN', b'Learn')])),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField()),
                ('description', models.TextField()),
                ('stars', models.IntegerField()),
                ('forks', models.IntegerField()),
                ('account', models.ForeignKey(to='hub.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('level', models.FloatField()),
                ('account', models.ForeignKey(to='hub.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='language',
            name='project',
            field=models.ForeignKey(to='hub.Project'),
        ),
        migrations.AddField(
            model_name='accountbadge',
            name='badge',
            field=models.ForeignKey(to='hub.Badge'),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('account', 'type', 'url')]),
        ),
        migrations.AlterUniqueTogether(
            name='contribution',
            unique_together=set([('account', 'url')]),
        ),
    ]
