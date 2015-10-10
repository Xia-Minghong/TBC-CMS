from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.incident_list),
    url(r'^(?P<inci_id>[0-9]+)/$', views.incident_detail), 
    url(r'^(?P<inci_id>[0-9]+)/updates/$', views.InciUpdate_list), 
    url(r'^[0-9]+/updates/(?P<inciUpdate_id>[0-9]+)/$', views.InciUpdate_detail), 
]