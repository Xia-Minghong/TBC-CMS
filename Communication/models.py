from django.db import models
from incident.models import Incident
# Create your models here.
# commmet1
class SocialMediaReport(models.Model):
    incident = models.ForeignKey(Incident)
    timestamp = models.DateTimeField('time published')
    socialMediaText = models.TextField()
