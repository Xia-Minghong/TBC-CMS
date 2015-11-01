from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.

class UpdatesViewSets(viewsets.ModelViewSet):
    queryset = UpdatesViewSets.objects.all()
    
    def create(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)

    