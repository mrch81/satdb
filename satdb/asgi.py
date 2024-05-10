#!/usr/bin/env python

"""
ASGI config for satdb project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import satapp.routing  # Import your application's routing module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'satdb.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            satapp.routing.websocket_urlpatterns
        )
    ),
})
