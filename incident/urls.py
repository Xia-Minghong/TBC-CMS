from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<incident_id>[0-9]+)/$', views.get_incident, name = 'get_incident')
]