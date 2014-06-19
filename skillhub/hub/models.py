from django.db import models

from django.contrib.auth.models import User


class Account(models.Model):
    class Meta:
        app_label = 'hub'


    user = models.OneToOneField(User)
    github_username = models.CharField(max_length=50)
    github_url = models.URLField()
    github_access_token = models.TextField()


class Skill(models.Model):
    class Meta:
        app_label = 'hub'

    account = models.ManyToManyField(Account)
    name = models.CharField(max_length=30)
    level = models.IntegerField()


class Tip(models.Model):
    class Meta:
        app_label = 'hub'

    name = models.CharField(max_length=50)
    description = models.TextField()

