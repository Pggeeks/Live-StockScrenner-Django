# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async,async_to_sync
from django_celery_beat.models import PeriodicTask , IntervalSchedule
class StockConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def addToCeleryBeat(self,Stock):
        task = PeriodicTask.objects.filter(name='every-1-seconds')
        if task:
            task = task.first()
            args = task.args
            args = args[0]
            task.args = json.dumps([Stock])
            task.save()
        else:
            schedule ,created=IntervalSchedule.objects.get_or_create(every=1,period=IntervalSchedule.SECONDS)
            task=PeriodicTask.objects.create(interval=schedule,name='every-1-seconds',task='stockapp.tasks.update_data',args=json.dumps(Stock))

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'stock_%s' % self.room_name
        self.room_group_name = 'StockDetails'
        self.StockName =self.scope['url_route']['kwargs']['StockName']

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        ## creating a celery beat task
        await self.addToCeleryBeat(self.StockName)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

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
        print(message)
        # Send message to WebSocket
        await self.send(json.dumps(message))