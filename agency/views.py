from agency.models import Agency
from agency.serializers import AgencySerializer
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    
    '''
    Create: POST http://127.0.0.1:8000/agencies/
    Read: GET http://127.0.0.1:8000/agencies/ or GET http://127.0.0.1:8000/agencies/agy_id
    Update: PUT http://127.0.0.1:8000/agencies/agy_id
    Delete: DELETE http://127.0.0.1:8000/agencies/agy_id
    
    '''
    def get_permissions(self):
        if self.action in ('list','retrieve'):
            self.permission_classes = [AllowAny,]
        return super(self.__class__, self).get_permissions()

    #GET http://127.0.0.1:8000/agencies/
    def list(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)
