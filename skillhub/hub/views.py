from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from constants import ProjectTypes
from hub.connect_github import ConnectGitHub
from hub.models import Account, Tip, Tutorial, Project
from hub.project_finder import ProjectFinder


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


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


class Practice(TemplateView):
    template_name = 'projects.html'

    def get(self, request):
        projects_found = ProjectFinder.find_my_projects(account, ProjectTypes.PRACTICE)
        projects = Project.objects.filter(account=request.user.account,
                                          type=ProjectTypes.PRACTICE)
        return render(request, self.template_name, {'projects': projects})


class Learn(TemplateView):
    template_name = 'projects.html'

    def get(self, request):
        projects_found = ProjectFinder.find_my_projects(account, ProjectTypes.LEARN)
        projects = Project.objects.filter(account=request.user.account,
                                         type=ProjectTypes.LEARN)
        return render(request, self.template_name, {'projects': projects})



