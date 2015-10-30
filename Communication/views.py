from django.shortcuts import render
from rest_framework import viewsets
from Communication.models import SocialMediaReport
from rest_framework import serializers
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from django.utils import timezone
from.media_publishers import MediaPublisherLoader
from incident.views import IncidentMgr, InciUpdateMgr, DispatchMgr


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
        incidents_data = IncidentMgr().recent_incidents()
        updates_data = InciUpdateMgr().recent_updates()
        dispatches_data = DispatchMgr().recent_dispatches()
        message = 'The testing is successful!!!\nTime tested: ' + time.ctime()

        message += ("\n\nRecent Incidents\n====================")
        for incident in incidents_data:
            message += ("\n")
            message += ("\nIncident   : " + incident["name"])
            message += ("\ntype       : " + incident["type"])
            message += ("\nStatus     : " + incident["status"])
            message += ("\nSeverity   : " + str(incident["severity"]))
            message += ("\nTime       : " + incident["time"])
            message += ("\nLocation   : " + incident["location"])
            message += ("\nDescription: " + incident["description"])
            message += ("\n")

        message += ("\n\nRecent Updates\n====================")
        for update in updates_data:
            message += ("\n")
            message += ("\nIncident        : " + update["incident"]["name"])
            message += ("\nUpdatd by       : " + update["agency"]["name"])
            message += ("\nStatus          : " + ("approved","pending")[update["is_approved"]])
            message += ("\nUpdated Severity: " + str(update["updated_severity"]))
            message += ("\nDescription     : " + update["description"])
            message += ("\n")

        message += ("\n\nRecent Dispatches\n====================")
        for dispatch in dispatches_data:
            message += ("\n")
            message += ("\nIncident         : " + dispatch["incident"]["name"])
            message += ("\nDispatched Agency: " + dispatch["agency"]["name"])
            message += ("\nResource         : " + dispatch["resource"])
            message += ("\nTime             : " + incident["time"])
            message += ("\n")
        return message

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


    TIME_INTERVAL = 10

    def periodically_publish(self,type):
        import time, threading
        threading.Timer(self.TIME_INTERVAL, lambda:self.periodically_publish(type)).start()
        message = self.publish(type)
        print("**********************\n" + time.ctime() + '\n' + message + "\n*********************")
