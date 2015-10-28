from django.db import models
from django.utils import timezone
# Create your models here.

class syslog(models.Model):
    name = models.CharField(max_length = 20)
    time = models.DateTimeField('time generated', default = timezone.now())
    generator = models.CharField(max_length = 50)
    description = models.TextField()