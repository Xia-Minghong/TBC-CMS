from rest_framework import serializers
from incident.models import Incident, InciUpdate

class IncidentSerializer(serializers.ModelSerializer):
    #default 'create' and 'update'
    class Meta:
        model = Incident
        
class InciUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InciUpdate