
import asyncio
from celery import shared_task
from celery_once import QueueOnce
from core.celery import app
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from nsetools import Nse
nse = Nse()
@shared_task(bind=True)
def update_data(self,stockpicked):
    nseQuote = nse.get_quote(stockpicked)
    Data = nseQuote['lastPrice']
    channels_layer = get_channel_layer()
    async_to_sync(channels_layer.group_send)(
        'StockDetails',
        {
        'type': 'stock_update',
        'message': Data
        }
    )
    return "done"
