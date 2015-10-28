from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Operator(models.Model):

    user = models.OneToOneField(User)

    name = models.CharField(max_length=100)

    operator_id = models.CharField(max_length=100)

    contact = models.CharField(max_length=20)

    img_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name + " : " + self.operator_id



class CrisisManager(models.Model):

    user = models.OneToOneField(User)

    name = models.CharField(max_length=100)

    contact = models.CharField(max_length=20)

    img_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class KeyDecisionMaker(models.Model):

    user = models.OneToOneField(User)

    name = models.CharField(max_length=100)

    position = models.CharField(max_length=20)

    img_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name + " : " + self.position