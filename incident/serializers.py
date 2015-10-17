from rest_framework import serializers
from .models import Incident, InciUpdate, Dispatch

class IncidentSerializer(serializers.ModelSerializer):
    #default 'create' and 'update'
    class Meta:
        model = Incident
        
class InciUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InciUpdate

class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch