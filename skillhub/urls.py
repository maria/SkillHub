from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from hub.views import HomeView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
