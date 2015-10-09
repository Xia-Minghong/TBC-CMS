from django.shortcuts import get_object_or_404

# Create your views here.
from incident.models import Incident
from django.http import HttpResponse
import json


def get_incident(request, incident_id):
    incident = get_object_or_404(Incident, pk = incident_id)
    return HttpResponse(json.dumps(incident.generate_json()), content_type = "application/json")