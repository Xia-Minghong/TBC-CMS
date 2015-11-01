from django.db import models
from agency.models import Agency
import django.utils
# Create your models here.

inci_type = (
                 ('haze', 'Haze'),
                 ('fire', 'Fire'),
                 ('crash', 'Crash'),
                 ('dengue', 'Dengue'), )

class Incident(models.Model):
    inci_status = (
                   ('initiated', 'initiated'), 
                   ('rejected', 'rejected'),
                   ('approved', 'approved'),
                   ('dispatched', 'dispatched'),
                   ('closed', 'closed'), )
    
    #operator = models.ForeignKey('operator') #operator yet to be created
    name = models.CharField(max_length = 50)
    status = models.CharField(max_length = 20, choices = inci_status, default = 'initiated')
    severity = models.IntegerField()
    time = models.DateTimeField('time reported', default = django.utils.timezone.now)
    location = models.CharField(max_length = 100)
    longitude = models.CharField(max_length = 50, default = '0')
    latitude = models.CharField(max_length = 50, default = '0')
    contact = models.CharField(max_length = 50)
    type = models.CharField(max_length = 50, choices = inci_type)
    description = models.TextField(blank = True)
    updates = models.ManyToManyField(Agency, through = 'InciUpdate', related_name = 'updatekeys+')
    dispatches = models.ManyToManyField(Agency, through = 'Dispatch', related_name = 'dispatch+')
    
    def __str__(self):
        return self.name
    
class InciUpdate(models.Model):
    incident = models.ForeignKey(Incident)
    agency = models.ForeignKey(Agency)
    is_approved = models.BooleanField(default = False)
    updated_severity = models.IntegerField()
    description = models.TextField()
    time = models.DateTimeField('time updated', default = django.utils.timezone.now)
    def __str__(self):
        return str(self.incident)
    
class Dispatch(models.Model):
    incident = models.ForeignKey(Incident)
    agency = models.ForeignKey(Agency)
    resource = models.TextField()
    time = models.DateTimeField('time dispatched', default = django.utils.timezone.now)
    def __str__(self):
        return str(self.incident)