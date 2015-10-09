from django.shortcuts import get_object_or_404

# Create your views here.
from incident.models import Incident, Agency
from django.http import HttpResponse
from App.serializers import Serializer
import json

def mani_incident(request, incident_id):
    if request.method == "GET":
        incident = get_object_or_404(Incident, pk = incident_id)
        serializer = Serializer()
        serialized = serializer.serialize([incident, ])
        return HttpResponse(serialized, content_type = "application/json")
    #if request.method == "POST":
        #for attribute in request.POST:
            

def get_agency(request, agency_id):
    agency = get_object_or_404(Agency, pk = agency_id)
    return HttpResponse(json.dumps(agency.generate_json()), content_type = "application/json")