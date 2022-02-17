
import asyncio
import re
from celery import shared_task
from celery_once import QueueOnce
from core.celery import app
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from nsetools import Nse
import schedule

nse = Nse()
def rr(self,stockpicked):
    schedule.every(1).seconds.do(update_data(stockpicked))
def update_data(self,stockpicked):
    print('rr')
    nseQuote= nse.get_quote(stockpicked)
    channels_layer = get_channel_layer()
    async_to_sync(channels_layer.group_send)(
       str(stockpicked),
        {
        'type': 'stock_update',
        'message': nseQuote,
        }
    )
def update_data(self,stockpicked):
    print('rr')
    nseQuote= nse.get_quote(stockpicked)
    channels_layer = get_channel_layer()
    async_to_sync(channels_layer.group_send)(
       str(stockpicked),
        {
        'type': 'stock_update',
        'message': nseQuote,
        }
    )
    return "done"
