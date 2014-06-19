import urllib2

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from hub.connect_github import ConnectGitHub


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
        code = urllib2.urlparse.parse_qsl(request.url)[-1][-1]
        account = ConnectGitHub().authorize(code)
        return HttpResponse({'status': 'OK'})
