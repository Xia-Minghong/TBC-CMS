from django.db import models
from agency.models import Agency
import django.utils
import os
# Create your models here.

inci_type = (
                 ('accident', 'Accident'),
                 ('fire', 'Fire'),
                 ('riot', 'Riot'),
                 ('gas_leak', 'Gas Leak'), )

class Incident(models.Model):
    inci_status = (
                   ('initiated', 'initiated'), 
                   ('approved', 'approved'),
                   ('dispatched', 'dispatched'),
                   ('rejected', 'rejected'),
                   ('closed', 'closed'), )
    
    #operator = models.ForeignKey('operator') #operator yet to be created
    name = models.CharField(max_length = 50)
    status = models.CharField(max_length = 20, choices = inci_status, default = 'initiated')
    severity = models.IntegerField()
    time = models.DateTimeField('time reported', default = django.utils.timezone.now)
    location = models.CharField(max_length = 100)
    longitude = models.CharField(max_length = 50, default = '0')
    latitude = models.CharField(max_length = 50, default = '0')

    contact_name = models.CharField(max_length=200, default="Unknown")
    contact = models.CharField(max_length = 50)
    type = models.CharField(max_length = 50, choices = inci_type)
    description = models.TextField(blank = True)
    agencies_through_inci_update = models.ManyToManyField(Agency, through = 'InciUpdate', related_name = 'updatekeys+')
    agencies_through_dispatch = models.ManyToManyField(Agency, through = 'Dispatch', related_name = 'dispatch+')
    
    def __str__(self):
        return self.name
    
class InciUpdate(models.Model):
    incident = models.ForeignKey(Incident)
    agency = models.ForeignKey(Agency)
    is_approved = models.BooleanField(default = False)
    updated_severity = models.IntegerField()
    description = models.TextField()
    time = models.DateTimeField('time updated', default = django.utils.timezone.now)
    photo_url = models.URLField(max_length = 500, default = '')
    def __str__(self):
        return "Incident: " + str(self.incident) + ",Agency: " + str(self.agency)
    
class Dispatch(models.Model):
    incident = models.ForeignKey(Incident)
    agency = models.ForeignKey(Agency)
    resource = models.TextField()
    is_approved = models.BooleanField(default = False)
    time = models.DateTimeField('time dispatched', default = django.utils.timezone.now)
    def __str__(self):
        return "Incident: " + str(self.incident) + ",Agency: " + str(self.agency)
    
class InciUpdatePhoto(models.Model):

    photo = models.FileField(upload_to = 'inci_update_photos')

    
    
