from django.urls import path , include
from app1.consumers import ChatConsumer


websocket_urlpatterns = [
    path("" , ChatConsumer.as_asgi()) , 
] 
