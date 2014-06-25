import datetime
import json

from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View

from constants import ProjectTypes
from hub.connect_github import ConnectGitHub
from helpers import get_projects, get_last_day
from hub.models import Account, Tip, Tutorial, Project, Contribution, AccountBadge
from hub.project_finder import ProjectFinder


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        data = {"sync": self._should_sync(request)}
        return render(request, self.template_name, data)

    def _should_sync(self, request):
        if hasattr(request.user, 'account'):
            if (not request.user.account.synced_at or
                    (request.user.account.synced_at - get_last_day()).days < 0):
                return True
        return False


class AuthorizeGitHub(TemplateView):

    def get(self, request):
        url = ConnectGitHub().authorize_url()
        return HttpResponseRedirect(url)


class ConnectGitHubAccount(TemplateView):

    def get(self, request):
        token = ConnectGitHub().get_access_token(request.GET['code'])
        account = Account.save_github_user(token)
        message = Account.login(request, account.user.username, token)
        return redirect("home")


class LogoutAccount(TemplateView):

    def get(self, request):
        logout(request)
        return redirect("home")


class SyncGithubData(View):

    def get(self, request):
        """Sync GitHub data for the account. Update contributions and projects.
        """
        account = request.user.account
        ProjectFinder.sync_account(account)
        return HttpResponse(content=json.dumps({"status": "ok"}),
                            content_type='application/javascript')


class Tips(TemplateView):
    template_name = 'tips.html'

    def get(self, request):
        tips = Tip.objects.all()
        return render(request, self.template_name, {'tips': tips})


class Tutorials(TemplateView):
    template_name = 'tutorials.html'

    def get(self, request):
        tutorials = Tutorial.objects.all()
        return render(request, self.template_name, {'tutorials': tutorials})


class AccountContributions(TemplateView):
    template_name = 'contributions.html'

    def get(self, request):
        contributions = Contribution.objects.filter(
            account=request.user.account).extra(order_by=['-merged'])
        return render(request, self.template_name, {'contributions': contributions})


class Practice(TemplateView):
    template_name = 'projects.html'

    def get(self, request):
        projects = get_projects(request.user.account, ProjectTypes.PRACTICE)
        return render(request, self.template_name, {'projects': projects})


class Learn(TemplateView):
    template_name = 'projects.html'

    def get(self, request):
        projects = get_projects(request.user.account, ProjectTypes.LEARN)
        return render(request, self.template_name, {'projects': projects})

class AccountBadges(TemplateView):
    template_name = 'badges.html'

    def get(self, request):
        account_badges = AccountBadge.objects.filter(account=request.user.account)
        badges = [account_badge.badge for account_badge in account_badges]
        return render(request, self.template_name, {'badges': badges})
