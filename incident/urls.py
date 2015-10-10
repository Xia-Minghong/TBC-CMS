from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.incident_list),
    url(r'^(?P<pk>[0-9]+)/$', views.incident_detail),
]