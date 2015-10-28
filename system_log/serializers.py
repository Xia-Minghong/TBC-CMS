from rest_framework import serializers
from .models import Syslog

class SyslogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Syslog