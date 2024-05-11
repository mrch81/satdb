#!/usr/bin/env python

"""WebSocket consumer module."""

import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class SatAppWsConsumer(AsyncWebsocketConsumer):
    """Channels WebSocket consumer for satapp."""

    async def connect(self):
        """Accept connection."""
        await self.accept()

    async def disconnect(self, close_code):
        """Disconnect websocket connection."""
        pass

    async def receive(self, text_data):
        """Receive webSocket connection."""
        pass

    async def satellite_updated(self, event):
        """Handle satellite_update event.

        Args:
            event (dict): contains info about the event

        """
        logger.debug("Satellite updated recieved")
        await self.send(text_data=json.dumps({'satellite_updated': event['satellite_updated']}))  # noqa: E501
