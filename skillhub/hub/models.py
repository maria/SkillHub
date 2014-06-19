from github import Github

from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    class Meta:
        app_label = 'hub'

    user = models.OneToOneField(User)
    github_username = models.CharField(max_length=50)
    github_url = models.URLField()
    github_access_token = models.TextField()

    @classmethod
    def save_github_user(cls, token):
        connection = Github(login_or_token=token).get_user()

        user = User(first_name=connection.name, email=connection.email)
        user.save()

        account = cls(user=user, github_access_token=token,
                      github_username=connection.name, github_url=connection.url)
        account.save()
        return account

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

