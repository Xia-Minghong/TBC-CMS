from rest_framework import serializers
from .models import Syslog

class SyslogReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Syslog
        exclude = ('description', )