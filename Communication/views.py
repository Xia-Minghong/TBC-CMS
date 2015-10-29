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


    #GET http://127.0.0.1:8000/publishers/type/send/
    @detail_route(methods=['get'])
    def send(self,request, *args, **kwargs):
        type = kwargs['pk']
        import time
        localtime = time.asctime( time.localtime(time.time()) )
        #localtime = timezone.localtime(timezone.now())
        message = 'The testing is successful!!!' + str(localtime)
        publisher = MediaPublisherLoader.load_publisher(type=type)
        return Response(publisher.compose_and_publish(message))
        #return Response(message)

