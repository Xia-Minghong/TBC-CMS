from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import list_route, detail_route
from .serializers import *
from rest_framework.response import Response


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


    # GET http://127.0.0.1:8000/users/me/
    @list_route(methods=['get'], permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, content_type="application/json")

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer