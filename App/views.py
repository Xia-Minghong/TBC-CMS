__author__ = 'WhiteHat'
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
import json

def index(request):
    return render(request, 'index.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
def publish(serializer, category):
    message = {}
    message[category] = serializer.data
    redis_publisher = RedisPublisher(facility = 'pushes', broadcast = True)
    redis_publisher.publish_message(RedisMessage(json.dumps(message)))