#!/usr/bin/env python

"""Test django models."""

from datetime import datetime

import pytest
from django.contrib.auth.models import User

from satapp.models import Launcher, Owner, Payload, Satellite


@pytest.mark.django_db
def test_owner_creation():
    """Create a new owner."""
    Owner.objects.create(name="Loft", country="France")
    assert Owner.objects.filter(name="Loft", country="France").exists() is True


@pytest.mark.django_db
def test_payload_creation():
    """Create a new payload."""
    sat = Satellite.objects.create(name="TOREDO")
    Payload.objects.create(satellite=sat,
                           provider="ESA",
                           type="virtual",
                           description="Process Methane data")
    assert Payload.objects.filter(satellite__id=sat.id,
                                  provider="ESA").exists() is True


@pytest.mark.django_db
def test_launcher_creation():
    """Create a new launcher."""
    sat = Satellite.objects.create(name="RONDA")
    launch_date = datetime(2024, 5, 9)
    launcher = Launcher.objects.create(launcher_type="SpaceX",
                                       launch_date=launch_date)
    launcher.satellites.add(sat)

    assert Launcher.objects.filter(launcher_type="SpaceX",
                                   launch_date=launch_date).exists() is True
    assert launcher in sat.launchers.all()


@pytest.mark.django_db
def test_satellite_creation():
    """Create a new satellite."""
    l1 = "1 25544U 98067A 08264.51782528 -.00002182  00000-0 -11606-4 0 2927"
    l2 = "2 25544 51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"
    owner = Owner.objects.create(name="Loft")
    Satellite.objects.create(name="YAMX",
                             sat_id="99999",
                             tle_date=datetime(2024, 5, 9),
                             line1=l1,
                             line2=l2,
                             owner=owner)

    sat = Satellite.objects.filter(name="YAMX",
                                   sat_id="99999")
    assert sat.exists() is True


@pytest.mark.django_db
def test_user_creation():
    """Create a new user."""
    User.objects.create(username="testuser")
    assert User.objects.filter(username="testuser").exists() is True
