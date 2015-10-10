from rest_framework import serializers
from incident.models import Incident

class IncidentSerializer(serializers.ModelSerializer):
    #default 'create' and 'update'
    class Meta:
        model = Incident