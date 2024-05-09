#!/usr/bin/env python

# Imports
from django.db import models


# Model definitions
class Owner(models.Model):
    """ Owner organization or company of the satellite """

    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)


class Satellite(models.Model):
    """
    Represents an individual satellite.

    Attributes:
        name (CharField): Name of the satellite. Length of 100 chars maximum
        owner (ForeignKey): A foreign key linking to the Owner model.

    Methods:
        __unicode__(self): Returns the satellite's name in string.
    """

    name = models.CharField(max_length=100)
    sat_id = models.IntegerField(null=True, unique=True)
    tle_date = models.DateTimeField(null=True, blank=True)
    line1 = models.CharField(max_length=69, null=True, blank=True)
    line2 = models.CharField(max_length=69, null=True, blank=True)
    owner = models.ForeignKey(Owner,
                              related_name='satellites',
                              on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        return "{}".format(self.name)


class Payload(models.Model):
    """ Satellite info """

    provider = models.CharField(max_length=120)
    satellite = models.ForeignKey(Satellite,
                                  related_name='payloads',
                                  on_delete=models.CASCADE)
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
