from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from settings import MEDIA_URL, MEDIA_ROOT

admin.autodiscover()

from hub.views import (HomeView, AuthorizeGitHub, ConnectGitHubAccount,
    LogoutAccount, Tips, Tutorials, Practice, Learn, AccountContributions,
    SyncGithubData)

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^authorize/', AuthorizeGitHub.as_view(), name='authorize'),
    url(r'^connect/', ConnectGitHubAccount.as_view(), name='connect'),
    url(r'^logout/', LogoutAccount.as_view(), name='logout'),
    url(r'^sync/', SyncGithubData.as_view(), name='sync'),
    url(r'^tips/', Tips.as_view(), name='tips'),
    url(r'^tutorials/', Tutorials.as_view(), name='tutorials'),
    url(r'^practice/', Practice.as_view(), name='practice'),
    url(r'^learn/', Learn.as_view(), name='learn'),
    url(r'^contributions/', AccountContributions.as_view(), name='contributions'),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
