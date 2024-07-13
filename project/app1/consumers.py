import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Channel
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_id = self.scope['url_route']['kwargs']['channel_id']
        self.channel_group_name = f'chat_{self.channel_id}'

        await self.channel_layer.group_add(
            self.channel_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.channel_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        user = await sync_to_async(User.objects.get)(username=username)
        channel = await sync_to_async(Channel.objects.get)(id=self.channel_id)
        message = await sync_to_async(Message.objects.create)(channel=channel, user=user, content=message)

        await self.channel_layer.group_send(
            self.channel_group_name, {
                "type": "sendMessage",
                "message": message.content,
                "username": message.user.username,
            })

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))
