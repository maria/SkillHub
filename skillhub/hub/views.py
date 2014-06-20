from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from hub.connect_github import ConnectGitHub
from hub.models import Account

class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        if not request.user.is_anonymous():
            data = {'user': {'username': request.user.username,
                             'url': request.user.account.github_url}
                    }
            return render(request, self.template_name, data)

        return render(request, self.template_name, {'user': None})


class AuthorizeGitHub(TemplateView):

    def get(self, request):
        url = ConnectGitHub().authorize_url()
        return HttpResponseRedirect(url)


class ConnectGitHubAccount(TemplateView):

    def get(self, request):
        token = ConnectGitHub().authorize(request.GET['code'])
        account = Account.save_github_user(token)
        message = Account.login(request, account.user.username, token)
        return redirect("home")


class LogoutAccount(TemplateView):

    def get(self, request):
        logout(request)
        return redirect("home")


class Tips(TemplateView):
    template_name = 'tips.html'

    def get(self, request):
        return render(request, self.template_name)


class Tutorials(TemplateView):
    template_name = 'tutorials.html'

    def get(self, request):
        return render(request, self.template_name)
