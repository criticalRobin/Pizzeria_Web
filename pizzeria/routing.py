from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path
from apps.api import consumers

websocket_urlpatterns = [
    path("ws/orders/", consumers.OrderConsumer.as_asgi()),
    re_path(r'ws/orders/update/$', consumers.OrderUpdateConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
