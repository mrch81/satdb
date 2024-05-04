""" TLE updater """

import asyncio
import logging
import threading

import aiohttp
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
            for data in tle_data:
                logger.info("Fetched satellite: %s", data)
                satellite, _ = Satellite.objects.get_or_create(
                                                    name=data['name'])
                # Update satellite properties with data from tle_data
                satellite.save()
                # Publish updates to subscribers
                await SatelliteSubscription.broadcast(
                           channel="satellite_updated",
                           payload={"satellite_updated": satellite.id})
            await asyncio.sleep(60)  # Fetch data every 60 seconds

    def start(self):
        t = threading.Thread(target=self._update_loop)
        t.daemon = True
        t.start()

    def _update_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.update_satellites())
