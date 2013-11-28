from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from core import views
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.index),
                       url(r'^login/?$', views.login),
                       url(r'^main/$', views.tracker),
                       url(r'^logout/?$', views.logout_view),
                       url(r'^reporting/$', views.reporting),
                       url(r'^ajax/$', views.ajax),
                       url(r'^overview/$', views.edit),
                       url(r'^password_change/$',
                           auth_views.password_change,
                           {'template_name': 'password_change_form.html'},
                           name='password_change'),
                       url(r'^password_change_done/$',
                           auth_views.password_change_done,
                           name='password_change_done'),
                       url(r'^(?P<drafttype>[a-z]{4})/(?P<dnumber>\d+)/(?P<language>[A-Z]{2})/$', views.draft),
                       url(r'^admin/', include(admin.site.urls)),
)
