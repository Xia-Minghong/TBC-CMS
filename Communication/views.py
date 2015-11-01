from django.shortcuts import render
from rest_framework import viewsets
from Communication.models import SocialMediaReport
from rest_framework import serializers
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from .managers import ReportMgr

class SocialMediaReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaReport

# Create your views here.
class SocialMediaReportViewSet(viewsets.ModelViewSet):
    queryset = SocialMediaReport.objects.all()
    serializer_class = SocialMediaReportSerializer
    
    def create(self, request, *args, **kwargs):
        response = viewsets.ModelViewSet.create(self, request, *args, **kwargs)
        
        return response

class PublisherViewSet(viewsets.ModelViewSet):

    queryset = SocialMediaReport.objects.all()
    serializer_class = SocialMediaReportSerializer
    '''need to edit the above'''


    #GET http://127.0.0.1:8000/publishers/type/send/
    @detail_route(methods=['get'])
    def send(self,request, *args, **kwargs):
        type = kwargs['pk']
        return Response(ReportMgr().publish(type))

    #GET http://127.0.0.1:8000/publishers/type/repeatedly_send/
    @detail_route(methods=['get'])
    def repeatedly_send(self,request, *args, **kwargs):
        type = kwargs['pk']
        ReportMgr().periodically_publish(type)
        return Response("haha")


