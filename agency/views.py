from django.shortcuts import get_object_or_404

# Create your views here.
from agency.models import Agency
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from agency.serializers import AgencySerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        

@csrf_exempt
def agency_list(request):
    if request.method == 'GET':
        agencies = Agency.objects.all()
        serializer = AgencySerializer(agencies, many = True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AgencySerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status = 201)
        return JSONResponse(serializer.errors(), status = 400)

@csrf_exempt
def agency_detail(request, pk):
    agency = get_object_or_404(Agency, pk = pk)
    if request.method == 'GET':
        serializer = AgencySerializer(agency)
        return JSONResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AgencySerializer(agency, data = data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors(), status = 400)
    elif request.methon == 'DELETE':
        agency.delete()
        return HttpResponse(status = 204)