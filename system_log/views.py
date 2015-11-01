from rest_framework import viewsets
from .models import Syslog
from .serializers import SyslogReadSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from App.views import publish

class SyslogViewSet(viewsets.ModelViewSet):
    queryset = Syslog.objects.all()
    serializer_class = SyslogReadSerializer
    
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
    
    
def push():
    queryset = Syslog.objects.order_by('-id')[0]
    serializer = SyslogReadSerializer(queryset)
    publish(serializer, "syslog")
        
def create_syslog(name, generator):
    syslog = Syslog(name = name, time = timezone.now(), generator = generator)
    syslog.save()
    push()
    
    
