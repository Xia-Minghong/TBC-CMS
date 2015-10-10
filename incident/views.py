from django.shortcuts import get_object_or_404

# Create your views here.
from incident.models import Incident, Agency
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from incident.serializers import IncidentSerializer

#from App.serializers import Serializer
#import json

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        
@csrf_exempt
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
def incident_detail(request, pk):
    incident = get_object_or_404(Incident, pk = pk)
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
    elif request.methon == 'DELETE':
        incident.delete()
        return HttpResponse(status = 204)

'''def mani_incident(request, incident_id):
    if request.method == "GET":
        incident = get_object_or_404(Incident, pk = incident_id)
        serializer = Serializer()
        serialized = serializer.serialize([incident, ])
        return HttpResponse(serialized, content_type = "application/json")
    if request.method == "POST":
        #request_content = json.loads(request.POST.body())
        return HttpResponse("post")#HttpResponse(request_content)
            

def mani_agency(request, agency_id):
    if request.method == "GET":
        agency = get_object_or_404(Agency, pk = agency_id)
        serializer = Serializer()
        serialized = serializer.serialize([agency, ])
        return HttpResponse(serialized, content_type = "application/json")'''