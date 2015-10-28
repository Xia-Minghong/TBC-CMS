from django.shortcuts import render
from rest_framework import viewsets
from Communication.models import SocialMediaReport
from rest_framework import serializers
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from django.utils import timezone
from.media_publishers import MediaPublisherLoader


class SocialMediaReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaReport

# Create your views here.
class SocialMediaReportViewSet(viewsets.ModelViewSet):
    queryset = SocialMediaReport.objects.all()
    serializer_class = SocialMediaReportSerializer


class PublisherViewSet(viewsets.ModelViewSet):

    queryset = SocialMediaReport.objects.all()
    serializer_class = SocialMediaReportSerializer
    '''need to edit the above'''


    #GET http://127.0.0.1:8000/communications/type/send/
    @detail_route(methods=['get'])
    def send(self,request, *args, **kwargs):
        type = kwargs['pk']
        time = timezone.localtime(timezone.now())
        message = 'The testing is successful!!!'# Message sent at: ' + str(time)
        publisher = MediaPublisherLoader.load_publisher(type=type)
        return Response(publisher.compose_and_publish(message))

