from .models import Incident, InciUpdate
from .serializers import IncidentSerializer, InciUpdateSerializer

from rest_framework import viewsets
from rest_framework.decorators import detail_route
#from rest_framework.response import Response

class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    
    #GET http://127.0.0.1:8000/incidents/inci_id/approve/
    #Approve an incident
    @detail_route(methods=['get'])
    def approve(self, request, pk = None):
        incident = Incident.objects.get(pk = pk)
        incident.status = 'approved'
        incident.save()
        self.queryset = Incident.objects.all().filter(id = pk)
        return viewsets.ModelViewSet.retrieve(self, request)
    
class InciUpdateViewSet(viewsets.ModelViewSet):
    queryset = InciUpdate.objects.all()
    serializer_class = InciUpdateSerializer
    
    #GET http://127.0.0.1:8000/incidents/inci_id/updates/
    def list(self, request, *args, **kwargs):
        cur_incident = Incident.objects.get(pk = kwargs['inci_id'])
        self.queryset = InciUpdate.objects.all().filter(incident = cur_incident)
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)
    
    #GET http://127.0.0.1:8000/incidents/inci_id/updates/inciUpdate_id/
    #Return one incident update associated with the incident specified according to its id
    def retrieve(self, request, *args, **kwargs):
        cur_incident = Incident.objects.get(pk = kwargs['inci_id'])
        self.queryset = InciUpdate.objects.all().filter(incident = cur_incident)
        return viewsets.ModelViewSet.retrieve(self, request, *args, **kwargs)
    
    #POST http://127.0.0.1:8000/incidents/inci_id/updates/
    #Regardless of the incident input, it will create an update under inci_id
    def create(self, request, *args, **kwargs):
        request.data['incident'] = kwargs['inci_id']
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)
    
    #GET http://127.0.0.1:8000/incidents/inci_id/updates/inciUpdate_id/approve/
    #Approve an incident update specified by inciUpdate_id
    @detail_route(methods=['get'])
    def approve(self, request, inci_id, pk = None):
        inci_update = InciUpdate.objects.get(pk = pk)
        inci_update.is_approved = True
        inci_update.save()
        self.queryset = InciUpdate.objects.all().filter(id = pk)
        return viewsets.ModelViewSet.retrieve(self, request)