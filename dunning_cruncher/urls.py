from django.conf.urls import patterns, include, url
from django.contrib import admin
from core import views
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.index),
                       url(r'^login/?$', views.login),
                       url(r'^main/?$', views.tracker),
                       url(r'logout/?$', views.logout_view),
                       url(r'reporting/?$', views.reporting),
    # url(r'^$', 'dunning_cruncher.views.home', name='home'),
    # url(r'^dunning_cruncher/', include('dunning_cruncher.foo.urls')),


    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
