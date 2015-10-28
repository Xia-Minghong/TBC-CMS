from django.db import models
import django.utils
# Create your models here.

class Syslog(models.Model):
    name = models.CharField(max_length = 20)
    time = models.DateTimeField('time generated', default = django.utils.timezone.now())
    generator = models.CharField(max_length = 50)
    description = models.TextField()