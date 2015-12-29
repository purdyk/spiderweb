from django.conf.urls import url

from . import views

from django.contrib.auth.views import login

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^groups/(?P<group_id>[0-9]+)$', views.group_detail, name='group_detail'),
    url(r'^groups/(?P<group_id>[0-9]+)/refresh$', views.group_refresh, name='group_refresh'),
    url(r'^results/(?P<result_id>[0-9]+)$', views.result_detail, name='result_detail'),
    url(r'^results/(?P<result_id>[0-9]+)/ignore$', views.result_ignore, name='result_ignore'),
    url(r'^reports/(?P<report_id>[0-9]+)/fetch$', views.report_fetch, name='report_fetch'),
    url(r'^accounts/login/$', login, name='login')
]
