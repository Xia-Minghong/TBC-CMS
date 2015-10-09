from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^incident/(?P<incident_id>[0-9]+)/$', views.mani_incident),
    url(r'^agency/(?P<agency_id>[0-9]+)/$', views.mani_agency)
]