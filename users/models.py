from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ConcreteUser(models.Model):

    user_types = (
                 ('operator', 'operator'),
                 ('kdm', 'kdm'),
                 ('crisis_manager', 'crisis_manager'),
                 )

    user = models.OneToOneField(User)

    type = models.CharField(max_length = 20, choices = user_types)

    name = models.CharField(max_length=100)

    operator_id = models.CharField(max_length=100, default="N.A.")

    contact = models.CharField(max_length=20, default="N.A.")

    position = models.CharField(max_length=20, default="N.A.")

    img_url = models.CharField(max_length=300, default="no image chosen")

    def __str__(self):
        return self.name + " : " + self.type

#
#
#
#
# class CrisisManager(models.Model):
#
#     user = models.OneToOneField(User)
#
#     name = models.CharField(max_length=100)
#
#     contact = models.CharField(max_length=20)
#
#     img_url = models.CharField(max_length=300)
#
#     def __str__(self):
#         return self.name
#
#
# class KeyDecisionMaker(models.Model):
#
#     user = models.OneToOneField(User)
#
#     name = models.CharField(max_length=100)
#
#     position = models.CharField(max_length=20)
#
#     img_url = models.CharField(max_length=300)
#
#     def __str__(self):
#         return self.name + " : " + self.position