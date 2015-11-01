from django.db import models
import incident
import agency
# Create your models here.

class updatesKeys(models.Model):
    incidentID = models.ForeignKey(incident.models.Incident)
    agencyID = models.ForeignKey(agency.models.Agency)
    keys = models.CharField()