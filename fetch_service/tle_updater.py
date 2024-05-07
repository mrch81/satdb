""" TLE updater """

import asyncio
import json
import logging

import aiohttp
import os
import django

from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "satdb.settings")
django.setup()

from satapp.models import Satellite
from satapp.schema import SatelliteSubscription
from satdb.settings import SATELLITE_FEED_URL

logger = logging.getLogger(__name__)


class TLEUpdater:
    def __init__(self):
        self.url = SATELLITE_FEED_URL

    async def fetch_tle_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                return await response.json()

    async def update_satellites(self):
        while True:
            tle_data = await self.fetch_tle_data()
            # Process the fetched data and update the satellites
            satellites = tle_data.get('member', [])
            for data in satellites:
                logger.info("Fetched satellite: %s", data)
                await sync_to_async(self.update_satellite)(data)
            await asyncio.sleep(60)  # Fetch data every 60 seconds

    def update_satellite(self, data):

        satellite, created = Satellite.objects.get_or_create(
                                                name=data['name'],
                                                sat_id=data['satelliteId'])  # noqa: E501
        # Update satellite properties with data from tle_data
        satellite.save()

        if created:
            # Publish updates to subscribers
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "satellite_update",
                {
                    "type": "satellite.updated",
                    "data": {
                        "id": satellite.id,
                        "sat_id": satellite.sat_id,
                        "name": satellite.name,
                        "tle_date": satellite.tle_date,
                        "line1": satellite.line1,
                        "line2": satellite.line2,
                    },
                }
            )

    async def run(self):
        await self.update_satellites()


if __name__ == "__main__":
    print("Run TLE fetcher")
    tle_updater = TLEUpdater()
    asyncio.run(tle_updater.run())
