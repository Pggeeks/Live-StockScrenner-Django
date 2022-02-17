# chat/consumers.py
from ast import Num, Pass, arg
from contextlib import nullcontext
from re import U
from channels.layers import get_channel_layer
from urllib.parse import parse_qs
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import AsyncToSync, sync_to_async , async_to_sync
from django_celery_beat.models import PeriodicTask , IntervalSchedule
from .models import  UsersCount
import uuid
from channels.exceptions import StopConsumer
from nsetools import Nse
class StockConsumer(AsyncWebsocketConsumer):
    # @sync_to_async
    # def Users_Count(self,group_name):
        # u = UsersCount.objects.get(Group_Name=group_name)
        # uid=uuid.uuid1()
        # print(uid)
        # u.Num_User += 1
        # u.save()
        # pass
        
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'stock_%s' % self.room_name
        self.StockName =self.scope['url_route']['kwargs']['StockName']
        self.room_group_name = self.StockName

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        ## creating a celery beat task
        await self.accept()
        # await self.Users_Count(self.room_group_name)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'stock_update',
                'message': message
            }
        )

    # Receive message from room group
    async def stock_update(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(json.dumps(message))