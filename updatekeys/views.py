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
    def create(self, request, *args, **kwargs):
        
        keyset = updatekeys.keysUtil.verifyKey(kwargs['key'])
        if not keyset:
            return Response(status= status.HTTP_401_UNAUTHORIZED)
        request.data['agency'] = keyset['agencyID']
        print request.data.__class__
        tempClass = incident.views.InciUpdateViewSet()
        tempClass.request = request
        tempClass.format_kwarg = kwargs
        return tempClass.create(request,args,inci_id = keyset["incidentID"])

    def list(self, request, *args, **kwargs):
        keyset = updatekeys.keysUtil.verifyKey(kwargs['key'])
        if not keyset:
            return Response(status= status.HTTP_401_UNAUTHORIZED)
        return Response({"true"})
        
    def retrieve(self, request, *args, **kwargs):
        
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def update(self, request, *args, **kwargs):
        print 'the one i needed'
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, *args, **kwargs):
        print 'this one?'
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
