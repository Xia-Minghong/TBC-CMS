from rest_framework import serializers
from .models import Incident, InciUpdate, Dispatch

class IncidentSerializer(serializers.ModelSerializer):
    #default 'create' and 'updatekeys'
    class Meta:
        model = Incident
        fields = ('name', 'status', 'severity', 'time', 'location', 'longitude', 'latitude', 'contact', 'contact', 'type', 'description', 'inciupdate_set', 'dispatch_set')

    #     name = models.CharField(max_length = 50)
    # status = models.CharField(max_length = 20, choices = inci_status, default = 'initiated')
    # severity = models.IntegerField()
    # time = models.DateTimeField('time reported', default = django.utils.timezone.now)
    # location = models.CharField(max_length = 100)
    # longitude = models.CharField(max_length = 50, default = '0')
    # latitude = models.CharField(max_length = 50, default = '0')
    # contact = models.CharField(max_length = 50)
    # type = models.CharField(max_length = 50, choices = inci_type)
    # description = models.TextField(blank = True)
    # updates = models.ManyToManyField(Agency, through = 'InciUpdate', related_name = 'updatekeys+')
    # dispatches = models.ManyToManyField(Agency, through = 'Dispatch', related_name = 'dispatch+')
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