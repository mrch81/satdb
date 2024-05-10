""" TLE updater """

import asyncio
import json
import logging
import os

import aiohttp
import django
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from typing import Any, Dict

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "satdb.settings")
django.setup()

from satapp.models import Satellite
from satapp.schema import SatelliteSubscription
from satdb.settings import FETCH_TLE_FREQUENCY, SATELLITE_FEED_URL

logger = logging.getLogger(__name__)


class TLEUpdater:
    """A service to fetch feeds from an Open API and update them."""

    def __init__(self) -> None:
        self.url: str = SATELLITE_FEED_URL

    async def fetch_tle_data(self) -> Dict[str, Any]:
        """ 
        Requests Satellite feed from SATELLITE_FEED_URL
        Returns the response json
        """
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                return await response.json()

    async def update_satellites(self) -> None:
        """ 
        Calls fetch data whose result is a json containing a list 
        of satellites. This is fed to update_satellite method to update.
        This is done at the frequency of FETCH_TLE_FREQUENCY seconds.
        """

        while True:
            tle_data: Dict[str, Any] = await self.fetch_tle_data()
            
            # Process the fetched data and update the satellites
            satellites: list = tle_data.get('member', [])
            for data in satellites:
                logger.info("Fetched satellite: %s", data['name'])
                await sync_to_async(self.update_satellite)(data)
            await asyncio.sleep(FETCH_TLE_FREQUENCY)  # Fetch data every 1 hour

    def update_satellite(self, data: Dict[str, Any]) -> None:
        """ 
        Updates satellite properties and publishes the satellite_update event
        to its subscribers
        """
        
        # Get the satellite object from our database or create it
        satellite, _ = Satellite.objects.get_or_create(
                                                name=data['name'],
                                                sat_id=data['satelliteId'])  # noqa: E501
        # Update satellite properties with data from tle_data
        satellite.tle_date = data['date']
        satellite.line1 = data['line2']
        satellite.line1 = data['line2']
        logger.debug("Satellite %r updated", satellite.sat_id)
        satellite.save()

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

    async def run(self) -> None:
        """ 
        Run the task that fetches the latest satellite data 
        and updating the local database or state
        """
        await self.update_satellites()


if __name__ == "__main__":
    logger.info("Run TLE fetcher")
    tle_updater = TLEUpdater()
    asyncio.run(tle_updater.run())
