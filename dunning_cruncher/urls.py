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
                           {'template_name': 'password_change_done.html'},
                           name='password_change_done'),
                       url(r'^(?P<drafttype>[a-z]{4})/(?P<dnumber>\d+)/(?P<language>[A-Z]{2})/$', views.draft),
                       url(r'^reminders/(?P<year>\d{4})/(?P<week>\d{2})/$', views.tracking_calendar),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^forgot_my_password/$', auth_views.password_reset,{'from_email':'admin@dunnings.com'}, name="forgot_my_password"),
                       url(r'^forgot_my_password_done/$', auth_views.password_reset_done,{'template_name': 'registration/password_reset_done.html'}, name="forgot_my_password_done"),
                       url(r'^forgot_my_password_confirm/(?P<uidb36>[0-9A-Za-z]+)\/(?P<token>.+)/$', auth_views.password_reset_confirm,
                           {'template_name': 'registration/password_reset_confirm.html'},name="forgot_my_password_confirm"),
                       url(r'^forgot_done/$', auth_views.password_reset_complete,{'template_name': 'registration/password_reset_complete.html'}, name="forgot_done"),
)
