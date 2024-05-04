#!/usr/bin/env python

import logging
from datetime import date

# Import
import graphene
from django.test import TestCase
from graphene.test import Client

from .models import Launcher, Owner, Payload, Satellite
from .schema import schema

logger = logging.getLogger(__name__)


class SatAppTestCase(TestCase):

    def setUp(self):
        # Create initial data (TODO: use fixtures)
        self.client = Client(schema)
        self.owner1 = Owner.objects.create(name="NASA", country="USA")
        self.owner2 = Owner.objects.create(name="ESA", country="Europe")
        
        self.satellite1 = Satellite.objects.create(id=1, name="Hubble", owner=self.owner1)
        self.satellite2 = Satellite.objects.create(id=2, name="YAM6", owner=self.owner2)
        self.payload1 = Payload.objects.create(provider="SpaceX",
                                               satellite=self.satellite1,
                                               type="Camera",
                                               description="High-resolution camera")
        self.launcher1 = Launcher.objects.create(launcher_type="Falcon 9", launch_date=date(2024, 3, 4))
        self.launcher1.satellites.add(self.satellite1)

    def test_query_all_satellites(self):
        response = self.client.execute('''
            query {
                allSatellites {
                    name
                    owner {
                        name
                    }
                }
            }
        ''')
        satellites = response.get('data').get('allSatellites')
        self.assertEqual(len(satellites), 2)
        self.assertEqual(satellites[0]['name'], 'Hubble')
        self.assertEqual(satellites[0]['owner']['name'], 'NASA')

    def test_create_satellite_mutation(self):
        response = self.client.execute('''
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
        ''' % self.owner1.pk)
        satellite = response.get('data').get('createSatellite').get('satellite')
        self.assertEqual(satellite['name'], 'James Webb')
        self.assertEqual(satellite['owner']['name'], 'NASA')

    def test_update_satellite_mutation(self):
        response = self.client.execute('''
            mutation {
                updateSatellite(id: %s, name: "Updated Hubble") {
                    satellite {
                        name
                    }
                }
            }
        ''' % self.satellite1.pk)
        satellite = response.get('data').get('updateSatellite').get('satellite')
        self.assertEqual(satellite['name'], 'Updated Hubble')

    def test_query_all_payloads(self):
        response = self.client.execute('''
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
        payloads = response.get('data').get('allPayloads')
        self.assertEqual(len(payloads), 1)
        self.assertEqual(payloads[0]['provider'], 'SpaceX')
        self.assertEqual(payloads[0]['type'], 'Camera')
        self.assertEqual(payloads[0]['description'], 'High-resolution camera')
        self.assertEqual(payloads[0]['satellite']['name'], 'Hubble')

    def test_create_payload_mutation(self):
        response = self.client.execute('''           
            mutation {
                createPayload(provider: "SpaceX", satelliteId: %s, type: "Camera", description: "High-resolution camera") {
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

        ''' % self.satellite1.pk)
        payloads = response.get('data').get('createPayload').get('payload')
        self.assertEqual(len(payloads), 5)
        self.assertEqual(payloads['provider'], 'SpaceX')
        self.assertEqual(payloads['type'], 'Camera')
        self.assertEqual(payloads['description'], 'High-resolution camera')
        self.assertEqual(payloads['satellite']['name'], 'Hubble')

    def test_update_payload_mutation(self):
        response = self.client.execute('''           
            mutation {
                updatePayload(id: %s, provider: "SpaceX", satelliteId: %s, type: "Camera", description: "High-resolution camera") {
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

        ''' % (self.payload1.pk, self.satellite1.pk))
        payload = response.get('data').get('updatePayload').get('payload')
        self.assertEqual(len(payload), 5)
        self.assertEqual(payload['provider'], 'SpaceX')
        self.assertEqual(payload['type'], 'Camera')
        self.assertEqual(payload['description'], 'High-resolution camera')
        self.assertEqual(payload['satellite']['name'], 'Hubble')

    def test_query_all_owners(self):
        response = self.client.execute('''
            query {
                allOwners {
                    name
                    country
                }
            }
        ''')
        owners = response.get('data').get('allOwners')
        self.assertEqual(len(owners), 2)
        self.assertEqual(owners[0]['name'], 'NASA')
        self.assertEqual(owners[0]['country'], 'USA')

    def test_create_owner_mutation(self):
        response = self.client.execute('''
            mutation {
                createOwner(name: "LOFT", country: "France") {
                    owner {
                        name
                        country
                    }                    
                }
            }
        ''')
        owner = response.get('data').get('createOwner').get('owner')
        self.assertEqual(owner['name'], 'LOFT')
        self.assertEqual(owner['country'], 'France')

    def test_update_owner_mutation(self):
        response = self.client.execute('''
            mutation {
                updateOwner(id: %s, name: "LeoStella", country: "Germany") {
                    owner {
                        name
                        country
                    }
                }
            }
        '''% self.owner1.pk)
        owner = response.get('data').get('updateOwner').get('owner')
        self.assertEqual(owner['name'], 'LeoStella')
        self.assertEqual(owner['country'], 'Germany')

    def test_query_all_launchers(self):
        response = self.client.execute('''
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
        launchers = response.get('data').get('allLaunchers')
        self.assertEqual(len(launchers), 1)
        self.assertEqual(launchers[0]['launcherType'], 'Falcon 9')
        self.assertEqual(launchers[0]['launchDate'], '2024-03-04')

    def test_create_launcher_mutation(self):
        response = self.client.execute('''
            mutation {
                createLauncher(launcherType: "Delta IV", launchDate: "2025-05-05", satelliteIds:[%s]) {
                    launcher {
                        launcherType
                        launchDate
                        satellites {
                            id
                        }
                    }
                }
            }
        ''' % self.satellite1.pk)
        
        launcher = response.get('data').get('createLauncher').get('launcher')
        self.assertEqual(launcher['launcherType'], 'Delta IV')
        self.assertEqual(launcher['launchDate'], '2025-05-05')
        self.assertEqual(launcher['satellites'][0]['id'], '1')

    def test_update_launcher_mutation(self):
        response = self.client.execute('''
            mutation {
                updateLauncher(id: %s, launcherType: "DeltaV", launchDate: "2025-06-06", satelliteIds:[%s]) {
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
        '''% (self.launcher1.pk, self.satellite2.pk))
        launcher = response.get('data').get('updateLauncher').get('launcher')
        self.assertEqual(launcher['launcherType'], 'DeltaV')
        self.assertEqual(launcher['launchDate'], '2025-06-06')
        self.assertEqual(launcher['satellites'][0]['id'], '2')
