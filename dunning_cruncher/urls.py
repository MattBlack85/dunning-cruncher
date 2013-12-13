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
                       url(r'^reporting/(?P<ryear>\d{4})/(?P<rmonth>\d+)/$', views.reporting),
                       url(r'^ajax/$', views.ajax),
                       url(r'^overview/$', views.edit),
                       url(r'^password_change/$',
                           auth_views.password_change,
                           {'template_name': 'password_change_form.html'},
                           name='password_change'),
                       url(r'^password_change_done/$',
                           auth_views.password_change_done,
                           {'template_name': 'password_change_done.html'},
                           name='password_change_done'),
                       url(r'^(?P<drafttype>[a-z]{4})/(?P<dnumber>\d+)/(?P<language>[A-Z]{2})/$', views.draft),
                       url(r'^reminders/(?P<year>\d{4})/(?P<week>\d+)/$', views.tracking_calendar),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^password_reset/$', auth_views.password_reset,
                           {'from_email': 'admin@dunnings.com'},
                           name="password_reset"),
                       url(r'^password_reset_done/$', auth_views.password_reset_done,
                           name="password_reset_done"),
                       url(r'password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)\/(?P<token>.+)/$', auth_views.password_reset_confirm,
                           name="password_reset_confirm"),
                       url(r'^password_reset_complete/$', auth_views.password_reset_complete,
                           name="password_reset_complete"),
)
