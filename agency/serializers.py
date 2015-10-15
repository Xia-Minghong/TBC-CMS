from rest_framework import serializers
from agency.models import Agency

class AgencySerializer(serializers.ModelSerializer):
    #To do: customize 'dispatched_by' & 'update_to'
    class Meta:
        model = Agency
