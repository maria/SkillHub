from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from hub.connect_github import ConnectGitHub
from hub.models import Account

class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        if hasattr(request, 'user') and not request.user.is_anonymous():
            data = {'user': {'username': request.user.account.github_username,
                             'url': user.account.github_url}
                    }
            return render(request, self.login_template_name, data)

        return render(request, self.template_name, {'user': None})


class AuthorizeGitHub(TemplateView):

    def get(self, request):
        url = ConnectGitHub().authorize_url()
        return HttpResponseRedirect(url)


class ConnectGitHubAccount(TemplateView):

    def get(self, request):
        token = ConnectGitHub().authorize(request.GET['code'])
        account = Account.save_github_user(token)
        account.login()
        return redirect("home")
