'''from django.core.serializers.json import Serializer as Builtin_Serializer

class Serializer(Builtin_Serializer):
    def get_dump_object(self, obj):
        return self._current'''
from django.contrib.auth.models import User, Group
from rest_framework import serializers

#class IncidentSerializer():