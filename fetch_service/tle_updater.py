""" TLE updater """

import asyncio
import logging

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
                satellite, _ = Satellite.objects.get_or_create(name=data['name'])  # noqa: E501
                # Update satellite properties with data from tle_data
                satellite.save()
                # Publish updates to subscribers
                await SatelliteSubscription.broadcast(
                                   channel="satellite_updated",
                                   payload={"satellite_updated": satellite.id})
            await asyncio.sleep(60)  # Fetch data every 60 seconds

    async def run(self):
        await self.update_satellites()


if __name__ == "__main__":
    print("Run TLE fetcher")
    tle_updater = TLEUpdater()
    asyncio.run(tle_updater.run())
