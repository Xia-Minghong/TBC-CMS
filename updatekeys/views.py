from rest_framework import viewsets, status
from updatekeys.models import updatesKeys
from rest_framework import serializers
from rest_framework.response import Response
import updatekeys.keysUtil,incident.views, incident.serializers

# Create your views here.
class updatesKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = updatesKeys




class UpdatesViewSets(viewsets.ModelViewSet):
    queryset = updatesKeys.objects.all()
    serializer_class = updatesKeySerializer
    
    
    #POST http://localhost:8000/update/<keys>/keys/
    # {"updated_severity" : 1, "description" : "hahah"}
    
    '''
    return the updated incident
    401 if the key is not valid
    '''
    
    def create(self, request, *args, **kwargs):
        
        keyset = updatekeys.keysUtil.verifyKey(kwargs['key'])
        if not keyset:
            return Response(status= status.HTTP_401_UNAUTHORIZED)
        if incident.models.Incident.objects.all().filter(id = keyset["incidentID"])[0].status == "closed":
            return Response('{"key expired"}',status= status.HTTP_401_UNAUTHORIZED)
        request.data['agency'] = keyset['agencyID']
        print request.data.__class__
        tempClass = incident.views.InciUpdateViewSet()
        tempClass.request = request
        tempClass.format_kwarg = kwargs
        return tempClass.create(request,args,inci_id = keyset["incidentID"])
    

    #GET http://localhost:8000/update/<keys>/keys/
    #return {"true"} if key is vaild, 401 otherwise
    def list(self, request, *args, **kwargs):
        keyset = updatekeys.keysUtil.verifyKey(kwargs['key'])
        if not keyset:
            return Response(status= status.HTTP_401_UNAUTHORIZED)
        import incident.views
        tempClass = incident.views.IncidentViewSet()
        tempClass.request = request
        kwargs['pk'] = keyset["incidentID"]
        tempClass.format_kwarg = self.format_kwarg
        tempClass.kwargs = kwargs
        return tempClass.retrieve(request,args,kwargs)
        
    def retrieve(self, request, *args, **kwargs):
        
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def update(self, request, *args, **kwargs):
        print 'the one i needed'
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, *args, **kwargs):
        print 'this one?'
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
