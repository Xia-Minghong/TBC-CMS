from django.db import models
from agency.models import Agency
import django.utils
import os
# Create your models here.

inci_type = (
                 ('haze', 'Haze'),
                 ('fire', 'Fire'),
                 ('crash', 'Crash'),
                 ('dengue', 'Dengue'), )

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
    
#     def path_and_rename(self, path):
#         def wrapper(instance, filename):
#             ext = filename.split('.')[-1]
#             if instance.pk:
#                 filename = '{}.{}'.format(str(django.utils.timezone.now), ext)
#             else:
#                 pass
#             return os.path.join(path, filename)
#         return wrapper
    
    photo = models.FileField(upload_to = 'inci_update_photos')
    #photo = models.FileField(upload_to = path_and_rename(path = '/inci_update_photos/'))
    inci_update = models.ForeignKey(InciUpdate)
    
    
