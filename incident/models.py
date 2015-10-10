from django.db import models
from agency.models import Agency
# Create your models here.

class Incident(models.Model):
    inci_status = (
                   ('init', 'initiated'), 
                   ('rej', 'rejected'),
                   ('appr', 'approved'),
                   ('disp', 'dispatched'),
                   ('closed', 'closed'), )
    inci_type = (
                 ('haze', 'haze'),
                 ('fire', 'fire'),
                 ('crash', 'crash'),
                 ('dengue', 'dengue'), )
    
    #operator = models.ForeignKey('operator') #operator yet to be created
    name = models.CharField(max_length = 50)
    status = models.CharField(max_length = 20, choices = inci_status)
    severity = models.IntegerField()
    time = models.DateTimeField('time reported')
    location = models.CharField(max_length = 100)
    contact = models.IntegerField()
    type = models.CharField(max_length = 50, choices = inci_type)
    description = models.TextField()
    updates = models.ManyToManyField(Agency, through = 'InciUpdate', related_name = 'update+')
    dispatches = models.ManyToManyField(Agency, through = 'Dispatch', related_name = 'dispatch+')
    
class InciUpdate(models.Model):
    incident = models.ForeignKey(Incident)
    agency = models.ForeignKey(Agency)
    is_approved = models.BooleanField(default = False)
    updated_severity = models.IntegerField()
    description = models.TextField()
    time = models.DateTimeField('time updated')
    
class Dispatch(models.Model):
    incident = models.ForeignKey(Incident)
    agency = models.ForeignKey(Agency)
    resource = models.TextField()
    time = models.DateTimeField('time dispatched')