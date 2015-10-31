from rest_framework import viewsets
from .models import Syslog
from .serializers import SyslogSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
import json

class SyslogViewSet(viewsets.ModelViewSet):
    queryset = Syslog.objects.all()
    serializer_class = SyslogSerializer
    
    #Syslog creation through URL is not allowed
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def list(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.retrieve(self, request, *args, **kwargs)
    
    #Syslog is not allowed to be updated
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    #Syslog is not allowed to be destroyed
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
def publish():
    queryset = Syslog.objects.order_by('-time')
    serializer = SyslogSerializer(queryset, many = True)
    redis_publisher = RedisPublisher(facility = 'syslogs', broadcast = True)
    redis_publisher.publish_message(RedisMessage(json.dumps(serializer.data)))
        
def create_syslog(name, generator, description):
    syslog = Syslog(name = name, time = timezone.now(), generator = generator, description = description)
    syslog.save()
    publish()
    
    
