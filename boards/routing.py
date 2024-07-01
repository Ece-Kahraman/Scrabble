from django.urls import re_path
from .consumers import *

websocket_urlpatterns = [
    re_path('ws/game/(?P<room_id>[0-9]+)/$', UpdateBoardConsumer.as_asgi()),
]
