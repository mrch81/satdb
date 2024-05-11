#!/usr/bin/env python

"""Define Django models here."""

# Imports
from django.db import models


# Model definitions
class Owner(models.Model):
    """
    Represents an owner company or oranization of the satellite.

    Attributes:
        name (CharField): Name of the owner/company (100 chars max).
        country (CharField): Name of the country of the owner (100 chars max).

    Methods:
        __unicode__(self): Returns the owner's name in string.
    """

    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __unicode__(self):  # noqa: D105
        return "{}".format(self.name)


class Satellite(models.Model):
    """
    Represents an individual satellite.

    Attributes:
        name (CharField): Name of the satellite. Length of 100 chars maximum.
        sat_id (CharField): Satellite ID.
        tle_date (CharField): Date when the last TLE update was made.
        line1 (CharField): Line 1 of TLE. Length of 69 chars maximum.
        line2 (CharField): Line 2 of TLE. Length of 69 chars maximum.
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

    def __unicode__(self):  # noqa: D105
        return "{}".format(self.name)


class Payload(models.Model):
    """
    Represents payload of the satellite.

    Attributes:
        provider (CharField): Name of the provider. 120 chars maximum.
        satellite (ForeignKey): A foreign key linking to the Satellite model.
        type (CharField): Name of the satellite. 120 chars maximum.
        description (TextField): A text describing the payload.

    Methods:
        __unicode__(self): Returns satellite's name and type of payload in str.
    """

    provider = models.CharField(max_length=120)
    satellite = models.ForeignKey(Satellite,
                                  related_name='payloads',
                                  on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):  # noqa: D105
        return "Satellite {} of type {}".format(self.satellite, self.type)


class Launcher(models.Model):
    """
    Represents Launcher of the satellite.

    Attributes:
        satellites (ManyToManyField): Linking to Satellite model.
        launcher_type (CharField): Type of the launcher. 100 chars maximum.
        launch_date (DateField): Date of the launch of the satellite.

    Methods:
        __unicode__(self): Returns the type of the launcher in string.
    """

    satellites = models.ManyToManyField(Satellite,  related_name='launchers')
    launcher_type = models.CharField(max_length=100)
    launch_date = models.DateField()

    def __unicode__(self):  # noqa: D105
        return "Launcher {}".format(self.launcher_type)
