from .models import Incident, InciUpdate, Dispatch
from .serializers import IncidentSerializer, InciUpdateSerializer, DispatchSerializer
from agency.models import Agency
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from Communication.outgoingSMS import sendingSMS
#from rest_framework.response import Response

class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    
    #POST http://127.0.0.1:8000/incidents/
    #Override create to ignore the input for status
    def create(self, request, *args, **kwargs):
        request.data['status'] = 'initiated'
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)
    
    #GET http://127.0.0.1:8000/incidents/inci_id/approve/
    #Approve an incident
    @detail_route(methods=['get'])
    def approve(self, request, pk = None):
        incident = Incident.objects.get(pk = pk)
        incident.status = 'approved'
        incident.save()
        self.queryset = Incident.objects.all().filter(id = pk)
        return viewsets.ModelViewSet.retrieve(self, request)
    
    #GET http://127.0.0.1:8000/incidents/inci_id/reject/
    #Reject an incident
    @detail_route(methods=['get'])
    def reject(self, request, pk = None):
        incident = Incident.objects.get(pk = pk)
        incident.status = 'rejected'
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
        request.data['is_approved'] = False
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
    
class DispatchViewSet(viewsets.ModelViewSet):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer
    
    #GET http://127.0.0.1:8000/incidents/inci_id/dispatches/
    def list(self, request, *args, **kwargs):
        cur_incident = Incident.objects.get(pk = kwargs['inci_id'])
        self.queryset = Dispatch.objects.all().filter(incident = cur_incident)
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)
    
    #POST http://127.0.0.1:8000/incidents/inci_id/dispatches/
    #Regardless of the incident input, it will create a dispatch under inci_id
    def create(self, request, *args, **kwargs):
        request.data['incident'] = kwargs['inci_id']
        incident = Incident.objects.get(pk = kwargs['inci_id'])
        incident.status = 'dispatched'
        incident.save()
        self.sendSMS(request, incident)
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)
    
    #GET http://127.0.0.1:8000/incidents/inci_id/dispatches/dispatch_id/
    #Return one dispatch associated with the incident specified by inci_id
    def retrieve(self, request, *args, **kwargs):
        cur_incident = Incident.objects.get(pk = kwargs['inci_id'])
        self.queryset = Dispatch.objects.all().filter(incident = cur_incident)
        return viewsets.ModelViewSet.retrieve(self, request, *args, **kwargs)

    def sendSMS(self, request, incident):
        agency = Agency.objects.get(pk = request.data['agency'])
        content = "Name: {} Location: {} Description: {} Resources: {}" \
            .format(incident.name, incident.location, incident.description, request.data['resource'])
        sendingSMS(content, '+65' + str(agency.contact))