from django.shortcuts import get_object_or_404

# Create your views here.
from .models import Incident, InciUpdate
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import IncidentSerializer, InciUpdateSerializer

from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from incident.models import InciUpdate

class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    
class InciUpdateViewSet(viewsets.ModelViewSet):
    queryset = InciUpdate.objects.all()
    serializer_class = InciUpdateSerializer
    
    #http://127.0.0.1:8000/incidents/inci_id/updates/
    def list(self, request, *args, **kwargs):
        cur_incident = Incident.objects.get(pk = kwargs['inci_id'])
        self.queryset = InciUpdate.objects.all().filter(incident = cur_incident)
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)
    
    #http://127.0.0.1:8000/incidents/inci_id/updates/inciUpdate_id/
    #Return one incident update associated with the incident specified according to its id
    def retrieve(self, request, *args, **kwargs):
        cur_incident = Incident.objects.get(pk = kwargs['inci_id'])
        self.queryset = InciUpdate.objects.all().filter(incident = cur_incident)
        return viewsets.ModelViewSet.retrieve(self, request, *args, **kwargs)