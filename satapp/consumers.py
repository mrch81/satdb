""" WebSocket consumer module"""

import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class SatAppWsConsumer(AsyncWebsocketConsumer):
    """Channels WebSocket consumer."""

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    async def satellite_updated(self, event):
        logger.debug("Satellite updated recieved")
        await self.send(text_data=json.dumps({'satellite_updated': event['satellite_updated']}))  # noqa: E501