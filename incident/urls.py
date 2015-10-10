from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^incidents/$', views.incident_list),
    url(r'^incidents/(?P<pk>[0-9]+)/$', views.incident_detail),
    url(r'^agencies/$', views.agency_list),
    url(r'^agencies/(?P<pk>[0-9]+)/$', views.agency_detail),
]