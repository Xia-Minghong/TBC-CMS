from .models import Incident, InciUpdate, Dispatch
from .models import inci_type
from .serializers import *
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
from django.utils import timezone
from App.views import publish

import updatekeys


RECENT_INTERVAL = datetime.timedelta(minutes=50)

#Push all incidents
def publish_incident(request):
    queryset = Incident.objects.exclude(status = 'closed')
    serializer = IncidentSerializer(queryset, many = True)
    publish(serializer, "incidents", request)
    
    
class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.exclude(status = 'closed')
    serializer_class = IncidentSerializer
    
    def push(self, request):
        publish_incident(request)

    #GET http://127.0.0.1:8000/incidents/id/
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = IncidentRetrieveSerializer
        return viewsets.ModelViewSet.retrieve(self, request, *args, **kwargs)

    #GET http://127.0.0.1:8000/incidents/
    def list(self, request, *args, **kwargs):
        self.serializer_class = IncidentListSerializer
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)

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
        incident, created = Incident.objects.get_or_create(**(request.data))
        if created:
            # self.push(request)
            create_syslog(name = "A Crisis Report<" + incident.name + "> Created", generator = request.user, request = request)
            from .notifiers import IncidentMgr
            IncidentMgr().notify(incident,message="create")
#             queryset = Incident.objects.order_by('-id')[0]
            print("=============type of queryset is : ")
            #print(str(type(queryset)))
            print("=============")
#             serializer = IncidentRetrieveSerializer(queryset)
            serializer = IncidentRetrieveSerializer(incident)
            return Response(serializer.data)
        else:
            return Response("incident creation failed")
        # response = viewsets.ModelViewSet.create(self, request, *args, **kwargs)
        # self.push(request)
        # new_incident = Incident.objects.order_by('-id')[0]
        # create_syslog(name = "A Crisis Report<" + new_incident.name + "> Created", generator = request.user, request = request)
        # self.propose_dispatch(request, new_incident)
        # return response
    
    
    #PUT http://127.0.0.1:8000/incidents/inci_id/
    # def update(self, request, *args, **kwargs):
    #     response = viewsets.ModelViewSet.update(self, request, *args, **kwargs)
    #     self.push(request)
    #     create_syslog(name = "A Crisis <" + self.get_object().name + "> Updated", generator = request.user, request = request)
    #     return response

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
        # self.push(request)
        create_syslog(name = "A Crisis Report <" + incident.name + "> Approved", generator = request.user, request = request)
        self.queryset = Incident.objects.all().filter(id = pk)
        from .notifiers import IncidentMgr, DispatchMgr
        IncidentMgr().notify(incident,"approve")
        DispatchMgr().propose_dispatch(incident)
        return viewsets.ModelViewSet.retrieve(self, request)

    @detail_route(methods=['get'])
    def archive(self, request, pk = None):
        incident = self.get_object()
        incident.status = 'closed'
        incident.save()
        self.push(request)
        create_syslog(name = "A Crisis Report <" + incident.name + "> Archived", generator = request.user, request = request)
        self.queryset = Incident.objects.filter(id = pk)
        return viewsets.ModelViewSet.retrieve(self, request)
    
    @detail_route(methods=['get'])
    def reject(self, request, pk = None):
        incident = self.get_object()
        incident.status = 'rejected'
        incident.save()
        self.push(request)
        create_syslog(name = "A Crisis Report <" + incident.name + "> Rejected", generator = request.user, request = request)
        self.queryset = Incident.objects.filter(id = pk)
        return viewsets.ModelViewSet.retrieve(self, request)
    
    #GET http://127.0.0.1:8000/incidents/recent/
    @list_route(methods=['get'])
    def recent(self, request, pk = None):
        return Response(IncidentMgr().recent_incidents(timedelta=RECENT_INTERVAL))

    @list_route(methods=['get'])
    def sync(self, request):
        # Sample code for reading incidents message queue
        redis_publisher = RedisPublisher(facility='pushes', broadcast=True)
        #message = redis_publisher.fetch_message(request, 'pushes')
        message = redis_publisher.fetch_message(request, facility='pushes')
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
        #return Response(data=message.replace("\\", ""))
    
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
    def alldispatches(self, request):
        queryset = Dispatch.objects.all().order_by('-time')
        serializer = DispatchSerializer(queryset, many = True)
        return Response(data = serializer.data)
        

    @list_route(methods=['get'])
    def test(self, request):
        IncidentMgr().notify()
        return Response("testing, haha")



class InciUpdateViewSet(viewsets.ModelViewSet):
    queryset = InciUpdate.objects.all()
    serializer_class = InciUpdateSerializer
    
    def push(self, request):
        queryset = InciUpdate.objects.all()
        serializer = self.get_serializer(queryset, many = True)
        publish(serializer, "updates", request)
    
    #GET http://127.0.0.1:8000/incidents/inci_id/updates/
    def list(self, request, *args, **kwargs):
        cur_incident = Incident.objects.get(pk = kwargs['inci_id'])
        self.queryset = InciUpdate.objects.all().filter(incident = cur_incident)
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)
    
    #GET http://127.0.0.1:8000/incidents/inci_id/updates/inciUpdate_id/
    #Return one incident updatekeys associated with the incident specified according to its id
    def retrieve(self, request, *args, **kwargs):
        cur_incident = Incident.objects.get(pk = kwargs['inci_id'])
        self.queryset = InciUpdate.objects.all().filter(incident = cur_incident)
        return viewsets.ModelViewSet.retrieve(self, request, *args, **kwargs)
    
    #POST http://127.0.0.1:8000/incidents/inci_id/updates/
    #Regardless of the incident input, it will create an updatekeys under inci_id
    def create(self, request, *args, **kwargs):
        print request.data.__class__
        
        request.data['incident'] = kwargs['inci_id']
        request.data['is_approved'] = False
        inci_update, created = InciUpdate.objects.get_or_create(**(request.data))
        if not created:
            return Response("inci_update creation failed")
        # self.serializer_class = InciUpdateWriteSerializer
        # response = viewsets.ModelViewSet.create(self, request, *args, **kwargs)
        incident = Incident.objects.get(pk = kwargs['inci_id'])
        incident.severity = request.data['updated_severity']
        incident.save()
        publish_incident(request)
        create_syslog(name = "A Crisis <" + incident.name + "> Updated", generator = request.user, request = request)
        from .notifiers import InciUpdateMgr
        IncidentMgr().notify(incident, inci_update)
        self.push(request)
        create_syslog(name = "A Crisis Update for <" + incident.name + "> Created", generator = request.user, request = request)
        serializer = InciUpdateSerializer(inci_update)
        return Response(serializer.data)
    
    #GET http://127.0.0.1:8000/incidents/inci_id/updates/inciUpdate_id/reject/
    #Approve an incident updatekeys specified by inciUpdate_id
    @detail_route(methods=['get'])
    def approve(self, request, inci_id, pk = None):
        inci_update = self.get_object()
        inci_update.is_approved = True
        inci_update.save()
        # self.push(request)
        create_syslog(name = "A Crisis Update for <" + inci_update.incident.name + "> Approved", generator = request.user, request = request)
        self.queryset = InciUpdate.objects.all().filter(id = pk)
        from .notifiers import InciUpdateMgr
        InciUpdateMgr().notify(object=inci_update, message="approve")
        return Response("Message successfully sent to {} at {}".format(inci_update.agency.name, inci_update.agency.contact))#viewsets.ModelViewSet.retrieve(self, request)

    #GET http://127.0.0.1:8000/incidents/inci_id/updates/inciUpdate_id/reject/
    #Reject and delte an incident update specified by inciUpdate_id
    @detail_route(methods=['get'])
    def reject(self, request, inci_id, pk = None):
        inci_update = self.get_object()
        inci_update.delete()
        # self.push(request)
        from .notifiers import InciUpdateMgr
        InciUpdateMgr().notify(inci_update, message="reject")
        create_syslog(name = "A Crisis Update for <" + inci_update.incident.name + "> Rejected and Deleted", generator = request.user, request = request)
        serializer = InciUpdateSerializer(inci_update)
        return Response(serializer.data)


class DispatchViewSet(viewsets.ModelViewSet):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer

    
    def push(self, request):
        queryset = Dispatch.objects.all()
        serializer = self.get_serializer(queryset, many = True)
        publish(serializer, "dispatches", request)
    
    #GET http://127.0.0.1:8000/incidents/inci_id/dispatches/
    def list(self, request, *args, **kwargs):
        cur_incident = Incident.objects.get(pk = kwargs['inci_id'])
        self.queryset = Dispatch.objects.all().filter(incident = cur_incident)
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)
    
    #POST http://127.0.0.1:8000/incidents/inci_id/dispatches/
    #Regardless of the incident input, it will create a dispatch under inci_id
    def create(self, request, *args, **kwargs):
        return Response("method not allowed")
        # request.data['incident'] = kwargs['inci_id']
        # self.serializer_class = DispatchWriteSerializer
        # response = viewsets.ModelViewSet.create(self, request, *args, **kwargs)
        # cur_incident = Incident.objects.get(pk = kwargs['inci_id'])
        # cur_incident.status = 'dispatched'
        # cur_incident.save()
        # publish_incident(request)
        #
        # #url for dispatch
        # specialURL = updatekeys.keysUtil.generateKey(kwargs['inci_id'], request.data['agency'])
        # print specialURL
        #
        # create_syslog(name = "A Crisis <" + cur_incident.name + "> Dispatched", generator = request.user, request = request)
        # self.push(request)
        # create_syslog(name = "A Crisis Dispatch for <" + cur_incident.name + "> Created", generator = request.user, request = request)
        #
        # self.sendSMS(request, cur_incident,specialURL)
        # '''from Communication.managers import DispatchSmsMgr
        # DispatchSmsMgr().publish(self.get_object(), type="SmsPublisher")'''
        # return response

    #GET http://127.0.0.1:8000/incidents/inci_id/dispatches/dispatch_id/
    #Return one dispatch associated with the incident specified by inci_id
    def retrieve(self, request, *args, **kwargs):
        cur_incident = Incident.objects.get(pk = kwargs['inci_id'])
        self.queryset = Dispatch.objects.all().filter(incident = cur_incident)
        return viewsets.ModelViewSet.retrieve(self, request, *args, **kwargs)

    #GET http://127.0.0.1:8000/incidents/inci_id/updates/dispatch_id/approve/
    #Approve an incident updatekeys specified by inciUpdate_id
    @detail_route(methods=['get'])
    def approve(self, request, inci_id, pk = None):
        dispatch = self.get_object()
        dispatch.is_approved = True
        dispatch.save()
        # self.push(request)
        create_syslog(name = "A Crisis Update for <" + dispatch.incident.name + "> Approved", generator = request.user, request = request)
        from .notifiers import DispatchMgr
        DispatchMgr().notify(object=dispatch, message="approve")
        self.queryset = InciUpdate.objects.all().filter(id = pk)
        return Response("Message successfully sent to {} at {}".format(dispatch.agency.name, dispatch.agency.contact))#viewsets.ModelViewSet.retrieve(self, request)

    #GET http://127.0.0.1:8000/incidents/inci_id/updates/inciUpdate_id/reject/
    #Reject and delte an incident update specified by inciUpdate_id
    @detail_route(methods=['get'])
    def reject(self, request, inci_id, pk = None):
        dispatch = self.get_object()
        dispatch.delete()
        # self.push(request)
        from .notifiers import DispatchMgr
        DispatchMgr().notify(object=dispatch, message="reject")
        create_syslog(name = "A Dispatch for <" + dispatch.incident.name + "> Rejected and Deleted", generator = request.user, request = request)
        serializer = DispatchSerializer(dispatch)
        return Response(serializer.data)


    def sendSMS(self, request, incident,url):
        agency = Agency.objects.get(pk = request.data['agency'])
        content = "{} Name: {} Location: {} Description: {} Resources: {}" \
            .format(url,incident.name, incident.location, incident.description, request.data['resource'])
        # from incident.
        sendingSMS(content, agency.contact)
