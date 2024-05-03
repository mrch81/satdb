#!/usr/bin/env python

# Imports
from django.db import models

# Model definitions
class Owner(models.Model):
    """
    Owner organization or company of the satellite
    """
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

class Satellite(models.Model):
    """
    Represents an individual satellite.

    Attributes:
        name (models.CharField): The name of the satellite. Maximum length of 100 characters.
        owner (models.ForeignKey): A foreign key linking to the Owner model, representing the owner of the satellite.
        
    Methods:
        __unicode__(self): Returns the satellite's name as its string representation.
        
    Example:
        >>> Satellite.objects.create(
                name="Sample Post",
                owner=Owner.objects.get(name="Loft"))
    """
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Owner, related_name='satellites', on_delete=models.CASCADE)

    def __unicode__(self):
        return "{}".format(self.name)

class Payload(models.Model):
    """
    Satellite info
    """
    provider = models.CharField(max_length=120)
    satellite = models.ForeignKey(Satellite, related_name='payloads', on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return "Satellite {} of type {}".format(self.satellite, self.type)

class Launcher(models.Model):
    satellites = models.ManyToManyField(Satellite,  related_name='launchers')
    launcher_type = models.CharField(max_length=100)
    launch_date = models.DateField()

    def __unicode__(self):
        return "Launcher {}".format(self.launcher_type)

