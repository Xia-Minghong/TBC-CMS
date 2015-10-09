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
    
    def generate_json(self):
        '''self_info = {}
        self_info['name'] = self.name
        self_info['status'] = self.status
        self_info['severity'] = self.severity
        self_info['time'] = str(self.time)
        self_info['location'] = self.location
        self_info['contact'] = self.contact
        self_info['type'] = self.type
        self_info['description'] = self.description
        return self_info'''
        
        return eval(self.__str__())
    
    def __str__(self):
        #pass
        return "{'name':'%s','status':'%s','severity':'%s','time':'%s','location':'%s','contact':'%s','type':'%s','description':'%s'}" \
                % (self.name, self.status, self.severity, str(self.time), self.location,
                   self.contact, self.type, self.description)
    
class Agency(models.Model):
    name = models.CharField(max_length = 50)
    contact = models.IntegerField()
    email = models.EmailField()
    dispatched_by = models.ManyToManyField(Incident, through = 'Dispatch', related_name = 'dispatch+')
    update_to = models.ManyToManyField(Incident, through = 'InciUpdate', related_name = 'update+')
    
    def generate_json(self):
        self_info = {}
        self_info['name'] = self.name
        self_info['contact'] = self.contact
        self_info['email'] = self.email
        return self_info
    
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
    