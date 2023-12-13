# """
# ASGI config for project project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# """

# import os
# import chat.routing
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter,URLRouter
# from channels.auth import AuthMiddlewareStack


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket":AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
            
#         )
#     )
    
# })
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lernr.settings")
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from .routing import websocket_urlpatterns

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': (
        URLRouter(routes=websocket_urlpatterns)
    )

})