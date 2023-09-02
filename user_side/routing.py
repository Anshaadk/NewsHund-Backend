from django.urls import re_path
from user_side import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
