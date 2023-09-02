import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from user_side.routing import websocket_urlpatterns  # Import your WebSocket routing configuration

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsHund.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Use your WebSocket routing configuration here
        )
    ),
})
