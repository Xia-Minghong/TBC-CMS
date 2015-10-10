from django.db import models
# Create your models here.
class Agency(models.Model):
    name = models.CharField(max_length = 50)
    contact = models.IntegerField()
    email = models.EmailField()