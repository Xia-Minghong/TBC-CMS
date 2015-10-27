from django.shortcuts import render
from rest_framework import viewsets
from Communication.models import SocialMediaReport
from rest_framework import serializers
from .models import MediaPublisherLoader
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response



class SocialMediaReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaReport

# Create your views here.
class SocialMediaReportViewSet(viewsets.ModelViewSet):
    queryset = SocialMediaReport.objects.all()
    serializer_class = SocialMediaReportSerializer

    #GET http://127.0.0.1:8000/communications/type/test_send/
    #Approve an incident update specified by inciUpdate_id
    @detail_route(methods=['get'])
    def test_send(self):
        fb = MediaPublisherLoader.load_publisher(type="FacebookPublisher")
        return Response(fb.compose_and_publish("message from Pycharm"))