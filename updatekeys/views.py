from django.shortcuts import render
from rest_framework import viewsets
from updatekeys.models import updatesKeys
from rest_framework import serializers
import hashlib
from incident.models import Incident
from agency.models import Agency

BASEURL = "http://cms.h5.io:8000/update/"

# Create your views here.
class updatesKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = updatesKeys

class UpdatesViewSets(viewsets.ModelViewSet):
    queryset = updatesKeys.objects.all()
    serializer_class = updatesKeySerializer
    def create(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)
    
def generateKey(incidentID , agencyID):
    print incidentID
    print agencyID
    incidentID = int(incidentID)
    agencyID = int(agencyID)
    
    keyObject = hashlib.md5()
    keyObject.update(incidentID.__str__() + '&' + agencyID.__str__())
    for _ in range(7):
        key = keyObject.hexdigest()
        keyObject = hashlib.md5()
        keyObject.update(key)
    keyInstance = updatesKeys(incidentID = Incident.objects.get(incidentID), angencyID = Agency.objects.get(agencyID), keys = key)
    keyInstance.save()
    return BASEURL + keyInstance.keys