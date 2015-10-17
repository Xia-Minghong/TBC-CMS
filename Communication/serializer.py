'''
Created on Oct 15, 2015

@author: Zhou
'''
from rest_framework import serializers
from Communication.models import SocialMediaReport

class SocialMediaReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaReport
    