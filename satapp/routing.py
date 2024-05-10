from django.urls import path

from satapp.consumers import SatAppWsConsumer

websocket_urlpatterns = [
    path('ws/satapp/', SatAppWsConsumer.as_asgi()),
]
