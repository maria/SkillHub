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
        user_data = cls._get_github_info(token)

        user = User.objects.create_user(
            first_name=user_data['first_name'], last_name=user_data['last_name'],
            email=user_data['email'],
            username=user_data['username'], password=token)

        account = cls(user=user, github_url=user_data['url'])
        account.save()
        return account

    @classmethod
    def login(cls, request, username, password):
        user = authenticate(username=username,
                            password=password)
        if user is not None and user.is_active:
            login(request, user)
            return {'message': "Account successfully logged in"}
        else:
            return {'message': "Account doesn't exist"}

    @classmethod
    def _get_github_info(cls, token):
        connection = Github(login_or_token=token).get_user()
        name = connection.name

        return {'email': connection.email, 'first_name': name.split(' ')[0],
                'last_name': name.split(' ')[1], 'url': connection.url,
                'username': connection.url.split('/')[-1]}

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

