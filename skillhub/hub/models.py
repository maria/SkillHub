from github import Github

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    class Meta:
        app_label = 'hub'

    user = models.OneToOneField(User)
    github_url = models.URLField()

    @classmethod
    def save_github_user(cls, token):
        connection = Github(login_or_token=token).get_user()
        username = connection.url.split('/')[-1]

        user = User(first_name=connection.name, email=connection.email,
                    username=username, password=token)
        user.save()

        account = cls(user=user, github_url=connection.url)
        account.save()

        return account

    def login(self):
        user = authenticate(username=self.user.username,
                            password=self.user.password)
        if user is not None and user.is_active:
            login(request, user)


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

