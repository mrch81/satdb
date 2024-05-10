#!/usr/bin/env python

import logging
from datetime import date

import pytest
from django.test import TestCase
from graphene.test import Client

from satapp.models import Launcher, Owner, Payload, Satellite
from satapp.schema import schema

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_query_all_satellites():

    client = Client(schema)
    owner1 = Owner.objects.create(name="NASA", country="USA")
    owner2 = Owner.objects.create(name="ESA", country="Europe")

    satellite1 = Satellite.objects.create(id=1,
                                               name="Hubble",
                                               owner=owner1)

    satellite2 = Satellite.objects.create(id=2,
                                               name="YAM6",
                                               owner=owner2)

    payload1 = Payload.objects.create(provider="SpaceX",
                                      satellite=satellite1,
                                      type="Camera",
                                      description="30M camera")

    launcher1 = Launcher.objects.create(launcher_type="Falcon 9",
                                        launch_date=date(2024, 3, 4))

    launcher1.satellites.add(satellite1)

    resp = client.execute('''
        query {
            allSatellites {
                name
                owner {
                    name
                }
            }
        }
    ''')
    satellites = resp['data'].get('allSatellites')
    assert len(satellites) == 2
    assert satellites[0]['name'] == 'Hubble'
    assert satellites[0]['owner']['name'] == 'NASA'

@pytest.mark.django_db
def test_create_satellite_mutation():
    client = Client(schema)
    owner1 = Owner.objects.create(name="NASA", country="USA")
    owner2 = Owner.objects.create(name="ESA", country="Europe")

    satellite1 = Satellite.objects.create(id=1,
                                          name="Hubble",
                                          owner=owner1)

    satellite2 = Satellite.objects.create(id=2,
                                          name="YAM6",
                                          owner=owner2)

    payload1 = Payload.objects.create(provider="SpaceX",
                                      satellite=satellite1,
                                      type="Camera",
                                      description="30M camera")

    launcher1 = Launcher.objects.create(launcher_type="Falcon 9",
                                             launch_date=date(2024, 3, 4))
    launcher1.satellites.add(satellite1)

    resp = client.execute('''
        mutation {
            createSatellite(name: "James Webb", ownerId: %s) {
                satellite {
                    name
                    owner {
                        name
                    }
                }
            }
        }
    ''' % owner1.pk)
    satellite = resp['data'].get('createSatellite').get('satellite')
    assert satellite['name'] == 'James Webb'
    assert satellite['owner']['name'] == 'NASA'

@pytest.mark.django_db
def test_update_satellite_mutation():
    client = Client(schema)
    owner1 = Owner.objects.create(name="NASA", country="USA")
    owner2 = Owner.objects.create(name="ESA", country="Europe")

    satellite1 = Satellite.objects.create(id=1,
                                               name="Hubble",
                                               owner=owner1)

    satellite2 = Satellite.objects.create(id=2,
                                          name="YAM6",
                                          owner=owner2)

    payload1 = Payload.objects.create(provider="SpaceX",
                                           satellite=satellite1,
                                           type="Camera",
                                           description="30M camera")

    launcher1 = Launcher.objects.create(launcher_type="Falcon 9",
                                             launch_date=date(2024, 3, 4))

    launcher1.satellites.add(satellite1)

    resp = client.execute('''
        mutation {
            updateSatellite(id: %s, name: "Updated Hubble") {
                satellite {
                    name
                }
            }
        }
    ''' % satellite1.pk)
    sat = resp['data'].get('updateSatellite').get('satellite')
    assert sat['name'] == 'Updated Hubble'

@pytest.mark.django_db
def test_query_all_payloads():
    client = Client(schema)
    owner1 = Owner.objects.create(name="NASA", country="USA")
    owner2 = Owner.objects.create(name="ESA", country="Europe")

    satellite1 = Satellite.objects.create(id=1,
                                               name="Hubble",
                                               owner=owner1)

    satellite2 = Satellite.objects.create(id=2,
                                               name="YAM6",
                                               owner=owner2)

    payload1 = Payload.objects.create(provider="SpaceX",
                                           satellite=satellite1,
                                           type="Camera",
                                           description="30M camera")

    launcher1 = Launcher.objects.create(launcher_type="Falcon 9",
                                             launch_date=date(2024, 3, 4))

    launcher1.satellites.add(satellite1)

    resp = client.execute('''
        query {
            allPayloads {
                provider
                type
                description
                satellite {
                    name
                }
            }
        }
    ''')
    payloads = resp['data'].get('allPayloads')
    assert len(payloads) == 1
    assert payloads[0]['provider'] == 'SpaceX'
    assert payloads[0]['type'] == 'Camera'
    assert payloads[0]['description'] == '30M camera'
    assert payloads[0]['satellite']['name'] == 'Hubble'

@pytest.mark.django_db
def test_create_payload_mutation():
    client = Client(schema)
    owner1 = Owner.objects.create(name="NASA", country="USA")
    owner2 = Owner.objects.create(name="ESA", country="Europe")

    satellite1 = Satellite.objects.create(id=1,
                                               name="Hubble",
                                               owner=owner1)

    satellite2 = Satellite.objects.create(id=2,
                                               name="YAM6",
                                               owner=owner2)

    payload1 = Payload.objects.create(provider="SpaceX",
                                           satellite=satellite1,
                                           type="Camera",
                                           description="30M camera")

    launcher1 = Launcher.objects.create(launcher_type="Falcon 9",
                                             launch_date=date(2024, 3, 4))

    launcher1.satellites.add(satellite1)

    resp = client.execute('''
        mutation {
            createPayload(provider: "SpaceX",
                          satelliteId: %s,
                          type: "Camera",
                          description: "High-resolution camera") {
              payload {
                id
                provider
                type
                description
                satellite {
                  id
                  name
                }
              }
            }
          }

    ''' % satellite1.pk)
    payloads = resp['data'].get('createPayload').get('payload')
    assert len(payloads) == 5
    assert payloads['provider'] == 'SpaceX'
    assert payloads['type'] == 'Camera'
    assert payloads['description'] == 'High-resolution camera'
    assert payloads['satellite']['name'] == 'Hubble'

@pytest.mark.django_db
def test_update_payload_mutation():
    client = Client(schema)
    owner1 = Owner.objects.create(name="NASA", country="USA")
    owner2 = Owner.objects.create(name="ESA", country="Europe")

    satellite1 = Satellite.objects.create(id=1,
                                               name="Hubble",
                                               owner=owner1)

    satellite2 = Satellite.objects.create(id=2,
                                               name="YAM6",
                                               owner=owner2)

    payload1 = Payload.objects.create(provider="SpaceX",
                                           satellite=satellite1,
                                           type="Camera",
                                           description="30M camera")

    launcher1 = Launcher.objects.create(launcher_type="Falcon 9",
                                             launch_date=date(2024, 3, 4))

    launcher1.satellites.add(satellite1)

    resp = client.execute('''
        mutation {
            updatePayload(id: %s,
                          provider:
                          "SpaceX",
                          satelliteId: %s,
                          type: "Camera",
                          description: "High-resolution camera") {
              payload {
                id
                provider
                type
                description
                satellite {
                  id
                  name
                }
              }
            }
          }

    ''' % (payload1.pk, satellite1.pk))
    payload = resp['data'].get('updatePayload').get('payload')
    assert len(payload) == 5
    assert payload['provider'] == 'SpaceX'
    assert payload['type'] == 'Camera'
    assert payload['description'] == 'High-resolution camera'
    assert payload['satellite']['name'] == 'Hubble'

@pytest.mark.django_db
def test_query_all_owners():
    client = Client(schema)
    owner1 = Owner.objects.create(name="NASA", country="USA")
    owner2 = Owner.objects.create(name="ESA", country="Europe")

    satellite1 = Satellite.objects.create(id=1,
                                               name="Hubble",
                                               owner=owner1)

    satellite2 = Satellite.objects.create(id=2,
                                               name="YAM6",
                                               owner=owner2)

    payload1 = Payload.objects.create(provider="SpaceX",
                                           satellite=satellite1,
                                           type="Camera",
                                           description="30M camera")

    launcher1 = Launcher.objects.create(launcher_type="Falcon 9",
                                             launch_date=date(2024, 3, 4))

    launcher1.satellites.add(satellite1)

    resp = client.execute('''
        query {
            allOwners {
                name
                country
            }
        }
    ''')
    owners = resp['data'].get('allOwners')
    assert len(owners) == 2
    assert owners[0]['name'] == 'NASA'
    assert owners[0]['country'] == 'USA'

@pytest.mark.django_db
def test_create_owner_mutation():
    client = Client(schema)
    owner1 = Owner.objects.create(name="NASA", country="USA")
    owner2 = Owner.objects.create(name="ESA", country="Europe")

    satellite1 = Satellite.objects.create(id=1,
                                               name="Hubble",
                                               owner=owner1)

    satellite2 = Satellite.objects.create(id=2,
                                               name="YAM6",
                                               owner=owner2)

    payload1 = Payload.objects.create(provider="SpaceX",
                                           satellite=satellite1,
                                           type="Camera",
                                           description="30M camera")

    launcher1 = Launcher.objects.create(launcher_type="Falcon 9",
                                             launch_date=date(2024, 3, 4))

    launcher1.satellites.add(satellite1)

    resp = client.execute('''
        mutation {
            createOwner(name: "LOFT", country: "France") {
                owner {
                    name
                    country
                }
            }
        }
    ''')
    owner = resp['data'].get('createOwner').get('owner')
    assert owner['name'] == 'LOFT'
    assert owner['country'] == 'France'

@pytest.mark.django_db
def test_update_owner_mutation():
    client = Client(schema)
    owner1 = Owner.objects.create(name="NASA", country="USA")
    owner2 = Owner.objects.create(name="ESA", country="Europe")

    satellite1 = Satellite.objects.create(id=1,
                                               name="Hubble",
                                               owner=owner1)

    satellite2 = Satellite.objects.create(id=2,
                                               name="YAM6",
                                               owner=owner2)

    payload1 = Payload.objects.create(provider="SpaceX",
                                           satellite=satellite1,
                                           type="Camera",
                                           description="30M camera")

    launcher1 = Launcher.objects.create(launcher_type="Falcon 9",
                                             launch_date=date(2024, 3, 4))

    launcher1.satellites.add(satellite1)

    resp = client.execute('''
        mutation {
            updateOwner(id: %s, name: "LeoStella", country: "Germany") {
                owner {
                    name
                    country
                }
            }
        }
    ''' % owner1.pk)
    owner = resp['data'].get('updateOwner').get('owner')
    assert owner['name'] == 'LeoStella'
    assert owner['country'] == 'Germany'

@pytest.mark.django_db
def test_query_all_launchers():
    client = Client(schema)
    owner1 = Owner.objects.create(name="NASA", country="USA")
    owner2 = Owner.objects.create(name="ESA", country="Europe")

    satellite1 = Satellite.objects.create(id=1,
                                               name="Hubble",
                                               owner=owner1)

    satellite2 = Satellite.objects.create(id=2,
                                               name="YAM6",
                                               owner=owner2)

    payload1 = Payload.objects.create(provider="SpaceX",
                                           satellite=satellite1,
                                           type="Camera",
                                           description="30M camera")

    launcher1 = Launcher.objects.create(launcher_type="Falcon 9",
                                             launch_date=date(2024, 3, 4))

    launcher1.satellites.add(satellite1)

    resp = client.execute('''
        query {
            allLaunchers {
                launcherType
                launchDate
                satellites {
                    name
                }
            }
        }
    ''')
    launchers = resp['data'].get('allLaunchers')
    assert len(launchers) == 1
    assert launchers[0]['launcherType'] == 'Falcon 9'
    assert launchers[0]['launchDate'] == '2024-03-04'

@pytest.mark.django_db
def test_create_launcher_mutation():
    client = Client(schema)
    owner1 = Owner.objects.create(name="NASA", country="USA")
    owner2 = Owner.objects.create(name="ESA", country="Europe")

    satellite1 = Satellite.objects.create(id=1,
                                               name="Hubble",
                                               owner=owner1)

    satellite2 = Satellite.objects.create(id=2,
                                               name="YAM6",
                                               owner=owner2)

    payload1 = Payload.objects.create(provider="SpaceX",
                                           satellite=satellite1,
                                           type="Camera",
                                           description="30M camera")

    launcher1 = Launcher.objects.create(launcher_type="Falcon 9",
                                             launch_date=date(2024, 3, 4))

    launcher1.satellites.add(satellite1)

    resp = client.execute('''
        mutation {
            createLauncher(launcherType: "Delta IV",
                           launchDate: "2025-05-05",
                           satelliteIds:[%s]) {
                launcher {
                    launcherType
                    launchDate
                    satellites {
                        id
                    }
                }
            }
        }
    ''' % satellite1.pk)

    launcher = resp['data'].get('createLauncher').get('launcher')
    assert launcher['launcherType'] == 'Delta IV'
    assert launcher['launchDate'] == '2025-05-05'
    assert launcher['satellites'][0]['id'] == '1'

@pytest.mark.django_db
def test_update_launcher_mutation():
    client = Client(schema)
    owner1 = Owner.objects.create(name="NASA", country="USA")
    owner2 = Owner.objects.create(name="ESA", country="Europe")

    satellite1 = Satellite.objects.create(id=1,
                                               name="Hubble",
                                               owner=owner1)

    satellite2 = Satellite.objects.create(id=2,
                                               name="YAM6",
                                               owner=owner2)

    payload1 = Payload.objects.create(provider="SpaceX",
                                           satellite=satellite1,
                                           type="Camera",
                                           description="30M camera")

    launcher1 = Launcher.objects.create(launcher_type="Falcon 9",
                                             launch_date=date(2024, 3, 4))

    launcher1.satellites.add(satellite1)

    resp = client.execute('''
        mutation {
            updateLauncher(id: %s,
                           launcherType: "DeltaV",
                           launchDate: "2025-06-06",
                           satelliteIds:[%s]) {
                launcher {
                    id
                    launcherType
                    launchDate
                    satellites {
                        id
                    }
                }
            }
        }
    ''' % (launcher1.pk, satellite2.pk))
    launcher = resp['data'].get('updateLauncher').get('launcher')
    assert launcher['launcherType'] == 'DeltaV'
    assert launcher['launchDate'] == '2025-06-06'
    assert launcher['satellites'][0]['id'] == '2'