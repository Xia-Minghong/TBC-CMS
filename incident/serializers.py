from rest_framework import serializers
from .models import Incident, InciUpdate, Dispatch

class IncidentSerializer(serializers.ModelSerializer):
    #default 'create' and 'updatekeys'

    # def __init__(self, *args, **kwargs):
    #     super(IncidentSerializer, self).__init__(
    #                             self, *args, **kwargs)
    #     try:
    #         self.Meta.depth = kwargs["depth"]
    #     except KeyError:
    #         self.Meta.depth = 0


    class Meta:
        model = Incident
        fields = ('id', 'name', 'status', 'severity', 'time', 'location', 'longitude', 'latitude', 'contact', 'contact', 'type', 'description', 'inciupdate_set', 'dispatch_set')
        depth = 0

class IncidentRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Incident
        fields = ('id', 'name', 'status', 'severity', 'time', 'location', 'longitude', 'latitude', 'contact', 'contact', 'type', 'description', 'inciupdate_set', 'dispatch_set')
        depth = 1
        
class InciUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InciUpdate
        depth = 1
        
class InciUpdateWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InciUpdate

class DispatchWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch

class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch
        depth = 1