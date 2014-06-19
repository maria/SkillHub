from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from hub.views import HomeView, AuthorizeGitHub, ConnectGitHubAccount

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^authorize/', AuthorizeGitHub.as_view(), name='authorize'),
    url(r'^connect/', ConnectGitHubAccount.as_view(), name='connect'),
    url(r'^admin/', include(admin.site.urls)),
)
