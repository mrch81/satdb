""" WebSocket consumer module"""

import json

from channels.generic.websocket import AsyncWebsocketConsumer


class SatAppWsConsumer(AsyncWebsocketConsumer):
    """Channels WebSocket consumer."""

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    async def satellite_updated(self, event):
        await self.send(text_data=json.dumps({'satellite_updated': event['satellite_updated']}))  # noqa: E501
