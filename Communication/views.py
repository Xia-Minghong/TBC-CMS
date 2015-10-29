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


    def generate_message(self):
        import time
        #localtime = time.asctime( time.localtime(time.time()) )
        #localtime = timezone.localtime(timezone.now())
        report = 'The testing is successful!!!' + time.ctime()
        return report

    def publish(self, type):
        message = self.generate_message()
        publisher = MediaPublisherLoader.load_publisher(type=type)
        return publisher.compose_and_publish(message)


    #GET http://127.0.0.1:8000/publishers/type/send/
    @detail_route(methods=['get'])
    def send(self,request, *args, **kwargs):
        type = kwargs['pk']
        return Response(self.publish(type))

    #GET http://127.0.0.1:8000/publishers/type/repeatedly_send/
    @detail_route(methods=['get'])
    def repeatedly_send(self,request, *args, **kwargs):
        type = kwargs['pk']
        self.periodically_publish(type)
        return Response("haha")


    TIME_INTERVAL = 8

    def periodically_publish(self,type):
        import time, threading
        print(time.ctime())
        self.publish(type)
        threading.Timer(self.TIME_INTERVAL, self.periodically_publish(type)).start()
