# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .views import *
class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['StockName']
        self.StockName =self.scope['url_route']['kwargs']['StockName']
        self.room_group_name = self.StockName

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        ## creating a celery beat task
        await self.accept()
        Show_Details.clearevent()
        # await self.Users_Count(self.room_group_name)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()
        Show_Details.Broken()
        

    # Receive message from WebSocket
    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        print(text_data)
        # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'stock_update',
        #         'message': message
        #     }
        # )

    # Receive message from room group
    async def stock_update(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(json.dumps(message))



###################################################
class AllStockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'Home'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        ## creating a celery beat task
        await self.accept()
        Home.clearevent()
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()
        # Show_Details.Broken()
        Home.Broken()
        print('dissc')
        

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(text_data)
       
    # Receive message from room group
    async def stock_update(self, event):
        await self.send(json.dumps(event))
