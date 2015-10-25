"""TheMachine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from rest_framework.routers import DefaultRouter
from agency.views import AgencyViewSet
from incident.views import IncidentViewSet, InciUpdateViewSet, DispatchViewSet
from . import views

router = DefaultRouter()
router.register(r'agencies', AgencyViewSet)
router.register(r'incidents', IncidentViewSet)
router.register(r'incidents/(?P<inci_id>[0-9]+)/updates', InciUpdateViewSet)
router.register(r'incidents/(?P<inci_id>[0-9]+)/dispatches', DispatchViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
]
