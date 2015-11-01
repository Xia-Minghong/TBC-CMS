from rest_framework import serializers
from .models import Incident, InciUpdate, Dispatch


class InciUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InciUpdate
        depth = 1

class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch
        depth = 1

class IncidentRetrieveSerializer(serializers.ModelSerializer):
    inciupdate_set = InciUpdateSerializer('inciupdate_set', many = True)
    dispatch_set = DispatchSerializer('dispatch_set', many = True)
    class Meta:
        model = Incident
        exclude = ('agencies_through_inci_update', 'agencies_through_dispatch')

class IncidentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Incident
        depth = 0

class IncidentListSerializer(serializers.ModelSerializer):
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

'''class IncidentRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Incident
        fields = ('id', 'name', 'status', 'severity', 'time', 'location', 'longitude', 'latitude', 'contact', 'contact', 'type', 'description', 'inciupdate_set', 'dispatch_set')
        depth = 2'''
        

        
class InciUpdateWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InciUpdate

class DispatchWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch

