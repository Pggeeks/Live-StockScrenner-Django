# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/Home', consumers.AllStockConsumer.as_asgi()),
    re_path(r'ws/stock/(?P<StockName>\w+)/$', consumers.StockConsumer.as_asgi()),
]
