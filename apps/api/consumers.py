# tu_app/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("orders", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("orders", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

    async def order_update(self, event):
        # Envía el mensaje a todos los clientes WebSocket conectados
        await self.send(text_data=json.dumps(event["message"]))
