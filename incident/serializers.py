from rest_framework import serializers
from incident.models import Incident, Agency

class IncidentSerializer(serializers.ModelSerializer):
    #default 'create' and 'update'
    class Meta:
        model = Incident

class AgencySerializer(serializers.ModelSerializer):
    #To do: customize 'dispatched_by' & 'update_to'
    class Meta:
        model = Agency