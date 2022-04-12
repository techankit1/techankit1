"""
ASGI config for GeniAnalysis project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from GeniAnalysis_app.routing import ws_urlpatterns
from asgiref.sync import sync_to_async
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GeniAnalysis.settings')
django.setup()

application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns))
})

# application = get_asgi_application()

