from .models import Incident, InciUpdate, Dispatch
from .models import inci_type
from .serializers import IncidentSerializer, InciUpdateSerializer, DispatchSerializer, InciUpdateWriteSerializer, DispatchWriteSerializer
from agency.models import Agency
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from Communication.outgoingSMS import sendingSMS
from rest_framework.response import Response
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from .notifiers import IncidentMgr
import json
import datetime
from system_log.views import create_syslog
from django.template.context_processors import request

RECENT_INTERVAL = datetime.timedelta(minutes=50)

#Push all incidents
def publish_incident():
    queryset = Incident.objects.all()
    serializer = IncidentSerializer(queryset, many = True)
    redis_publisher = RedisPublisher(facility = 'incidents', broadcast = True)
    redis_publisher.publish_message(RedisMessage(json.dumps(serializer.data)))
    
    
class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    
    def publish(self):
        publish_incident()
    
    #POST http://127.0.0.1:8000/incidents/
    #Override create to ignore the input for status
    '''Return
    {
    "id": 17,
    "name": "push",
    "status": "approved",
    "severity": 2,
    "time": "2015-10-31T06:17:14Z",
    "location": "sth",
    "contact": "98",
    "type": "fire",
    "description": "ss",
    "updates": [],
    "dispatches": []
    }
    '''
    def create(self, request, *args, **kwargs):
        request.data['status'] = 'initiated'
        response = viewsets.ModelViewSet.create(self, request, *args, **kwargs)
        self.publish()
        new_incident = Incident.objects.order_by('-id')[0]
        serializer = self.get_serializer(new_incident)
        create_syslog(name = "Create an Incident", generator = request.user, description = json.dumps(serializer.data).replace('\"', ''))
        return response
    
    #PUT http://127.0.0.1:8000/incidents/inci_id/
    def update(self, request, *args, **kwargs):
        response = viewsets.ModelViewSet.update(self, request, *args, **kwargs)
        self.publish()
        serializer = self.get_serializer(self.get_object())
        create_syslog(name = "Update an Incident", generator = request.user, description = json.dumps(serializer.data).replace('\"', ''))
        return response

    #GET http://127.0.0.1:8000/incidents/inci_id/approve/
    #Approve an incident
    '''Return
    {
    "id": 17,
    "name": "push",
    "status": "approved",
    "severity": 2,
    "time": "2015-10-31T06:17:14Z",
    "location": "sth",
    "contact": "98",
    "type": "fire",
    "description": "ss",
    "updates": [],
    "dispatches": []
    }
    '''
    @detail_route(methods=['get'])
    def approve(self, request, pk = None):
        incident = self.get_object()
        incident.status = 'approved'
        incident.save()
        self.publish()
        serializer = self.get_serializer(incident)
        create_syslog(name = "Approve an Incident", generator = request.user, description = json.dumps(serializer.data).replace('\"', ''))
        self.queryset = Incident.objects.all().filter(id = pk)
        return viewsets.ModelViewSet.retrieve(self, request)

    #GET http://127.0.0.1:8000/incidents/recent/
    @list_route(methods=['get'])
    def recent(self, request, pk = None):
        return Response(IncidentMgr().recent_incidents(timedelta=RECENT_INTERVAL))

    #GET http://127.0.0.1:8000/incidents/inci_id/reject/
    #Reject an incident
    '''Return
    {
    "id": 28,
    "name": "push6",
    "status": "rejected",
    "severity": 5,
    "time": "2015-10-30T16:21:15Z",
    "location": "swh",
    "contact": "123",
    "type": "haze",
    "description": "NA",
    "updates": [],
    "dispatches": []
    }
    '''
    @detail_route(methods=['get'])
    def reject(self, request, pk = None):
        incident = self.get_object()
        incident.status = 'rejected'
        incident.save()
        self.publish()
        serializer = self.get_serializer(incident)
        create_syslog(name = "Reject an Incident", generator = request.user, description = json.dumps(serializer.data).replace('\"', ''))        
        self.queryset = Incident.objects.all().filter(id = pk)
        return viewsets.ModelViewSet.retrieve(self, request)
    


    @list_route(methods=['get'])
    def sync(self, request):
        # Sample code for reading incidents message queue
        redis_publisher = RedisPublisher(facility='dispatches', broadcast=True)

        message = redis_publisher.fetch_message(request, 'dispatches')
        # if the message is empty, replace it with a empty json/dict and convert to a string
        if not message:
            message = json.dumps({})
        # message = json.loads(message)
        #
        # message['first_name'] = 'zzzz'
        #
        # message = RedisMessage(json.dumps(message))
        # redis_publisher.publish_message(message)

        return Response(json.loads(message))
    
    #GET http://127.0.0.1:8000/incidents/types/
    '''Return
    [
    {
        "value": "haze",
        "title": "Haze"
    },
    {
        "value": "fire",
        "title": "Fire"
    },
    {
        "value": "crash",
        "title": "Crash"
    },
    {
        "value": "dengue",
        "title": "Dengue"
    }
    ]
    '''
    @list_route(methods=['get'])
    def types(self, request):
        result = []
        for item in inci_type:
            each_type = dict(zip(['value', 'title'], list(item)))
            result.append(each_type)
        return Response(data = result)
    
    @list_route(methods=['get'])
    def allupdates(self, request):
        queryset = InciUpdate.objects.all().order_by('-time')
        serializer = InciUpdateSerializer(queryset, many = True)
        return Response(data = serializer.data)
        

    @list_route(methods=['get'])
    def test(self, request):
        IncidentMgr().notify()
        return Response("testing, haha")


class InciUpdateViewSet(viewsets.ModelViewSet):
    queryset = InciUpdate.objects.all()
    serializer_class = InciUpdateSerializer
    
    def publish(self):
        queryset = InciUpdate.objects.all()
        serializer = self.get_serializer(queryset, many = True)
        redis_publisher = RedisPublisher(facility = 'inciupdates', broadcast = True)
        redis_publisher.publish_message(RedisMessage(json.dumps(serializer.data)))
    
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
        self.serializer_class = InciUpdateWriteSerializer
        response = viewsets.ModelViewSet.create(self, request, *args, **kwargs)
        cur_incident = Incident.objects.get(pk = kwargs['inci_id'])
        cur_incident.severity = request.data['updated_severity']
        cur_incident.save()
        publish_incident()
        inci_serializer = IncidentSerializer(cur_incident)
        create_syslog(name = "Update an Incident via an Incident Update", generator = request.user, description = json.dumps(inci_serializer.data).replace('\"', ''))
        self.publish() 
        new_inciUpdate = InciUpdate.objects.order_by('-id')[0]
        serializer = self.get_serializer(new_inciUpdate)
        create_syslog(name = "Create an Incident Update", generator = request.user, description = json.dumps(serializer.data).replace('\"', ''))
        return response
    
    #GET http://127.0.0.1:8000/incidents/inci_id/updates/inciUpdate_id/approve/
    #Approve an incident update specified by inciUpdate_id
    @detail_route(methods=['get'])
    def approve(self, request, inci_id, pk = None):
        inci_update = self.get_object()
        inci_update.is_approved = True
        inci_update.save()
        self.publish()
        serializer = self.get_serializer(inci_update)
        create_syslog(name = "Approve an Incident Update", generator = request.user, description = json.dumps(serializer.data).replace('\"', ''))
        self.queryset = InciUpdate.objects.all().filter(id = pk)
        return viewsets.ModelViewSet.retrieve(self, request)
    
class DispatchViewSet(viewsets.ModelViewSet):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer
    
    def publish(self):
        queryset = Dispatch.objects.all()
        serializer = self.get_serializer(queryset, many = True)
        redis_publisher = RedisPublisher(facility = 'dispatches', broadcast = True)
        redis_publisher.publish_message(RedisMessage(json.dumps(serializer.data)))
    
    #GET http://127.0.0.1:8000/incidents/inci_id/dispatches/
    def list(self, request, *args, **kwargs):
        cur_incident = Incident.objects.get(pk = kwargs['inci_id'])
        self.queryset = Dispatch.objects.all().filter(incident = cur_incident)
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)
    
    #POST http://127.0.0.1:8000/incidents/inci_id/dispatches/
    #Regardless of the incident input, it will create a dispatch under inci_id
    def create(self, request, *args, **kwargs):
        request.data['incident'] = kwargs['inci_id']
        self.serializer_class = DispatchWriteSerializer
        response = viewsets.ModelViewSet.create(self, request, *args, **kwargs)
        cur_incident = Incident.objects.get(pk = kwargs['inci_id'])
        cur_incident.status = 'dispatched'
        cur_incident.save()
        publish_incident()
        inci_serializer = IncidentSerializer(cur_incident)
        create_syslog(name = "Dispatch an Incident", generator = request.user, description = json.dumps(inci_serializer.data).replace('\"', ''))
        self.publish()
        new_dispatch = Dispatch.objects.order_by('-id')[0]
        serializer = self.get_serializer(new_dispatch)
        create_syslog(name = "Create an Incident Dispatch", generator = request.user, description = json.dumps(serializer.data).replace('\"', ''))
        self.sendSMS(request, cur_incident)
        return response
    
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
        sendingSMS(content, agency.contact)
