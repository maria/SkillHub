import arrow
from github import Github

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import models

from constants import ProjectTypes, MAX_PROJECTS



class TimestampFields(models.Model):
    '''
        An abstract model to include in your model class
        for time tracking goodness. Includes the tracking
        fields:
        - created_at (when the instance was created)
        - updated_at (when the instance was last written in
                      the database)
    '''

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, null=True,
                                      blank=True, help_text='When this '
                                      'instance was created')
    updated_at = models.DateTimeField(auto_now=True, null=True,
                                      blank=True, help_text='When this '
                                      'instance was last updated')

class Account(TimestampFields):
    class Meta:
        app_label = 'hub'

    user = models.OneToOneField(User)
    github_url = models.URLField()
    github_token = models.TextField()
    avatar_url = models.TextField()
    synced_at = models.DateTimeField(null=True, blank=True)

    @classmethod
    def save_github_user(cls, token):
        user_data = cls._get_github_info(token)
        user = cls.get_user(token)

        if user is not None:
            return user.account

        user = User.objects.create_user(
            first_name=user_data['first_name'], last_name=user_data['last_name'],
            email=user_data['email'],
            username=user_data['username'], password=token)

        account = cls(user=user, github_url=user_data['url'],
                      github_token=token, avatar_url=user_data['avatar_url'])
        account.save()
        return account

    @classmethod
    def get_user(cls, token):
        user_data = cls._get_github_info(token)

        users = User.objects.filter(username=user_data['username'])

        if len(users) is 1:
            user = users[0]
            if user.account.github_token != token:
                user.password = token
                user.save()

                user.account.token = token
                user.account.save()
            return user

        return None

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
                'last_name': name.split(' ')[1], 'url': connection.html_url,
                'avatar_url': connection.avatar_url,
                'username': connection.html_url.split('/')[-1]}



class Project(TimestampFields):

    class Meta:
        app_label = 'hub'
        unique_together = ('account', 'type', 'url')

    account = models.ForeignKey(Account)
    type = models.CharField(max_length=30, choices=tuple(ProjectTypes.items()))
    name = models.CharField(max_length=50)
    url = models.URLField()
    description = models.TextField()
    stars = models.IntegerField()
    forks = models.IntegerField()

    @property
    def languages(self):
        return self.language_set.all()[:3]

    @property
    def languages_names(self):
        return [language.name for language in self.languages]


class Contribution(TimestampFields):

    class Meta:
        app_label = 'hub'
        unique_together = ('account', 'url')

    account = models.ForeignKey(Account)
    title = models.TextField()
    url = models.URLField()
    merged = models.DateTimeField()
    repo = models.CharField(max_length=50)
    repo_url = models.URLField()

    @property
    def merged_date(self):
        return arrow.formatter.DateTimeFormatter().format(self.merged, 'YYYY-MM-DD')


class Language(models.Model):
    class Meta:
        app_label = 'hub'
        unique_together = ('project', 'name')

    project = models.ForeignKey(Project)
    name = models.CharField(max_length=50)
    percentage = models.FloatField()


class Skill(models.Model):
    class Meta:
        app_label = 'hub'
        unique_together = ('account', 'name')

    account = models.ForeignKey(Account)
    name = models.CharField(max_length=30)
    level = models.IntegerField()


class Tip(models.Model):
    class Meta:
        app_label = 'hub'

    name = models.CharField(max_length=50)
    description = models.TextField()


class Tutorial(models.Model):
    class Meta:
        app_label = 'hub'

    name = models.CharField(max_length=50)
    description = models.TextField()
    url = models.URLField()




