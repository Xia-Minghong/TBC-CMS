from django.db import models

# Create your models here.
import ast

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
    
class Agency(models.Model):
    name = models.CharField(max_length = 50)
    contact = models.IntegerField()
    email = models.EmailField()
    dispatched_by = models.ManyToManyField(Incident, through = 'Dispatch', related_name = 'dispatch+')
    update_to = models.ManyToManyField(Incident, through = 'InciUpdate', related_name = 'update+')
    
class InciUpdate(models.Model):
    incident = models.ForeignKey(Incident)
    agency = models.ForeignKey(Agency)
    is_approved = models.BooleanField(default = False)
    updated_severity = models.IntegerField()
    description = models.TextField()
    time = models.DateTimeField('time updated')
    #updated_by = models.CharField(max_length = 20)
    
class Dispatch(models.Model):
    incident = models.ForeignKey(Incident)
    agency = models.ForeignKey(Agency)
    resource = models.TextField()
    time = models.DateTimeField('time dispatched')
    