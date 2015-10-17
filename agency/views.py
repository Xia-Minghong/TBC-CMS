from agency.models import Agency
from agency.serializers import AgencySerializer
from rest_framework import viewsets

class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    
    '''
    Create: POST http://127.0.0.1:8000/agencies/
    Read: GET http://127.0.0.1:8000/agencies/ or GET http://127.0.0.1:8000/agencies/agy_id
    Update: PUT http://127.0.0.1:8000/agencies/agy_id
    Delete: DELETE http://127.0.0.1:8000/agencies/agy_id
    
    '''