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

class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    
    '''@detail_route()
    def updates(self, request, pk = None):
        inci_updates = InciUpdate.objects.all().filter(incident = pk)
        serializer = InciUpdateSerializer(inci_updates, many = True)
        return Response(serializer.data)'''

class InciUpdateViewSet(viewsets.ModelViewSet):
    queryset = InciUpdate.objects.all()
    serializer_class = InciUpdateSerializer
        
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        
'''@csrf_exempt
def incident_list(request):
    if request.method == 'GET':
        incidents = Incident.objects.all()
        serializer = IncidentSerializer(incidents, many = True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = IncidentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status = 201)
        return JSONResponse(serializer.errors(), status = 400)

@csrf_exempt
def incident_detail(request, inci_id):
    incident = get_object_or_404(Incident, pk = inci_id)
    if request.method == 'GET':
        serializer = IncidentSerializer(incident)
        return JSONResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = IncidentSerializer(incident, data = data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors(), status = 400)
    elif request.method == 'DELETE':
        incident.delete()
        return HttpResponse(status = 204)
    '''
@csrf_exempt
def InciUpdate_list(request, inci_id):
    if request.method == 'GET':
        incident = get_object_or_404(Incident, pk = inci_id)
        inci_updates = incident.inciupdate_set.all()
        serializer = InciUpdateSerializer(inci_updates, many = True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = InciUpdateSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status = 201)
        return JSONResponse(serializer.errors(), status = 400)
    
@csrf_exempt
def InciUpdate_detail(request, inciUpdate_id):
    inci_update = get_object_or_404(InciUpdate, pk = inciUpdate_id)
    if request.method == 'GET':
        serializer = InciUpdateSerializer(inci_update)
        return JSONResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = InciUpdateSerializer(inci_update, data = data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors(), status = 400)
    elif request.method == 'DELETE':
        inci_update.delete()
        return HttpResponse(status = 204)