from rest_framework import serializers
from .models import Incident, InciUpdate, Dispatch

from .models import InciUpdatePhoto

class InciUpdatePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InciUpdatePhoto

class InciUpdateSerializer(serializers.ModelSerializer):
    inciupdatephoto_set = InciUpdatePhotoSerializer('inciupdatephoto_set', many = True)
    class Meta:
        model = InciUpdate
        depth = 1

class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch
        depth = 1

class InciUpdateWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InciUpdate

class DispatchWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch

class IncidentRetrieveSerializer(serializers.ModelSerializer):
    inciupdate_set = InciUpdateSerializer('inciupdate_set', many = True)
    dispatch_set = DispatchSerializer('dispatch_set', many = True)
    class Meta:
        model = Incident
        exclude = ('agencies_through_inci_update', 'agencies_through_dispatch')
        
class IncidentListSerializer(serializers.ModelSerializer):
    inciupdate_set = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    dispatch_set = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    class Meta:
        model = Incident
        exclude = ('agencies_through_inci_update', 'agencies_through_dispatch')

class IncidentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Incident



'''class IncidentListSerializer(serializers.ModelSerializer):
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
        depth = 0'''

'''class IncidentRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Incident
        fields = ('id', 'name', 'status', 'severity', 'time', 'location', 'longitude', 'latitude', 'contact', 'contact', 'type', 'description', 'inciupdate_set', 'dispatch_set')
        depth = 2'''
        

        


