from django.db import models
# Create your models here.

class Syslog(models.Model):
    name = models.CharField(max_length = 200)
    time = models.DateTimeField('time generated')
    generator = models.CharField(max_length = 50)
    #description = models.TextField()