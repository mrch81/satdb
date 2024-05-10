#!/usr/bin/env python

"""Generate fixtures for Owners, Satellites, Payloads, and Launchers."""

import datetime
import json
import os
from random import choice, randint

from django.apps import apps
from django.core.management.base import BaseCommand
from faker import Faker

# Random Line1 (from TLE)
L1 = ["1 99999U 24029BR  24131.97222222  .00001103 00000-0 33518-4 0  9998",
      "1 99999U 24029BR  44131.97222222  .00001103 00000-0  33518-4 0 8998",
      "1 99999U 24029BR  64131.97222222  .00001103 00000-0  33518-4 0 7998",
      "1 99999U 24029BR  74131.97222222  .00001103 00000-0  33518-4 0 6998",
      "1 99999U 24029BR  74131.97222222  .00001103 00000-0  33518-4 0 5998",
      "1 99999U 24029BR  25131.97222222  .00001103 00000-0  33518-4 0 4998",
      "1 99999U 24029BR  33131.97222222  .00001103 00000-0  33518-4 0 3998",
      ]

# Random Line2 (from TLE)
L2 = ["2 99999 53.00000   0.7026 0003481 299.7327   0.3331 15.07816962  1770",
      "2 99999 53.00000   0.6036 0003481 299.7327   9.3331 15.07816962  2770",
      "2 99999 53.00000   0.8036 0003481 299.7327  18.3331 15.07816962  3771",
      "2 99999 53.00000   0.9036 0003481 299.7327  27.3331 15.07816962  4771",
      "2 99999 53.00000   0.7066 0003481 299.7327  36.3331 15.07816962  5771",
      "2 99999 53.00000   0.7024 0003481 299.7327  45.3331 15.07816962  6771",
      "2 99999 53.00000   0.5455 0003481 299.7327  54.3331 15.07816962  7771",
      ]


class Command(BaseCommand):
    """Class to handle django's custom manage command."""

    help = 'Generates fixtures for Owners, Satellites, Payloads, and Launchers'

    def handle(self, *args, **options):
        """Generate data and create json."""
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
            today = datetime.datetime.today()
            dates = [today - datetime.timedelta(days=x) for x in range(10)]
            for i in range(num):
                satellites.append({
                    "model": "satapp.satellite",
                    "pk": i + 1,
                    "fields": {
                        "name": f"{fake.word().capitalize()} Satellite",
                        "owner": randint(1, owners_count),
                        "sat_id": randint(11111, num_entries),
                        "tle_date": choice(dates),
                        "Line1": choice(L1),
                        "Line2": choice(L2),
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


if __name__ == "__main__":
    pass
