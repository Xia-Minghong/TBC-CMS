from rest_framework import viewsets
from .models import Syslog
from .serializers import SyslogSerializer
from rest_framework.response import Response
from rest_framework import status

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
    
    def create_log(self):
        pass
    
    
