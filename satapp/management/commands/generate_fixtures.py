#!/usr/bin/env python

import json
import os
from random import choice, randint

from django.apps import apps
from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    help = 'Generates fixtures for Owners, Satellites, Payloads, and Launchers'

    def handle(self, *args, **options):
        app_config = apps.get_app_config('satapp')
        fixtures_dir = os.path.join(app_config.path, 'fixtures')

        # Check if the fixtures directory exists, and create it if it does not
        os.makedirs(fixtures_dir, exist_ok=True)

        # Generate fixtures
        Faker.seed(0)
        fake = Faker()

        def generate_owners(num):
            return [{
                "model": "satapp.owner",
                "pk": i + 1,
                "fields": {
                    "name": fake.company(),
                    "country": fake.country()
                }
            } for i in range(num)]

        def generate_satellites(num, owners_count):
            satellites = []
            for i in range(num):
                satellites.append({
                    "model": "satapp.satellite",
                    "pk": i + 1,
                    "fields": {
                        "name": f"{fake.word().capitalize()} Satellite",
                        "owner": randint(1, owners_count)
                    }
                })
            return satellites

        def generate_payloads(num, satellites_count):
            payload_types = ['Camera',
                             'Sensor',
                             'Mirror',
                             'Antenna',
                             'Solar Panel',
                             'RGB Imager']

            payload_providers = ['Eutelsat',
                                 'Kineis',
                                 'Totum',
                                 'Airbus',
                                 'Santal',
                                 'Pixie']

            payload_descr = ["For high resolution pictures",
                             "Methan presence sensors",
                             "Reflects lights to generate enegery",
                             "Inter satellite communication",
                             "For motor one",
                             "Detects water presence",]

            payloads = []
            for i in range(num):
                payloads.append({
                    "model": "satapp.payload",
                    "pk": i + 1,
                    "fields": {
                        "provider": choice(payload_providers),
                        "satellite": randint(1, satellites_count),
                        "type": choice(payload_types),
                        "description": choice(payload_descr),
                    }
                })
            return payloads

        def generate_launchers(num, satellites_count):
            launcher_types = ['Space Shuttle',
                              'SpaceX',
                              'Falcon 9',
                              'Ariane 5',
                              'Soyuz',
                              'Long March']

            launchers = []
            for i in range(num):
                launchers.append({
                    "model": "satapp.launcher",
                    "pk": i + 1,
                    "fields": {
                        "satellites": [randint(1, satellites_count)],
                        "launcher_type": choice(launcher_types),
                        "launch_date": fake.date()
                    }
                })
            return launchers

        # Call generate methods
        num_entries = 100
        owners = generate_owners(num_entries)
        satellites = generate_satellites(num_entries, len(owners))
        payloads = generate_payloads(num_entries, len(satellites))
        launchers = generate_launchers(num_entries, len(satellites))

        # Save fixtures data into json
        with open(os.path.join(fixtures_dir, 'owners.json'), 'w') as f:
            json.dump(owners, f, indent=4)

        with open(os.path.join(fixtures_dir, 'satellites.json'), 'w') as f:
            json.dump(satellites, f, indent=4)

        with open(os.path.join(fixtures_dir, 'payloads.json'), 'w') as f:
            json.dump(payloads, f, indent=4)

        with open(os.path.join(fixtures_dir, 'launchers.json'), 'w') as f:
            json.dump(launchers, f, indent=4)

        self.stdout.write(self.style.SUCCESS('Fixtures generated'))


def main():
    pass


if __name__ == "__main__":
    main()
