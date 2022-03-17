from datetime import datetime
import uuid
from django.views import View
from channels.layers import get_channel_layer
from bs4 import BeautifulSoup
from ast import Break, arg

from asgiref.sync import async_to_sync
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import schedule
import time
import json
from threading import Thread
import requests
from nsetools import Nse
from threading import Thread, Event
nse = Nse()
# Create your views here.


class Home(View):
    def get(self, request):
        global stop_event
        AllStocks = nse.get_stock_codes()
        a = {"RELIANCE": "RELIANCE INDUSTRIES", "HDFCBANK": "HDFC BANK", "INFY": "INFOSYS",
             "ICICIBANK": "ICICI BANK", "TCS": "TATA CONSULTANCY SERVICES", "LT": "LARSEN & TOUBRO LTD"}
        Data = [nse.get_quote(i) for i in a ]
        Nifty50 = nse.get_index_quote("nifty 50")
        NiftyBank = nse.get_index_quote("nifty Bank")
        stop_event = Event()  # for geting the current event
        # make a thread to get prices
        s = Thread(target=self.SendPrices, args=(a,))
        s.daemon = True
        s.start()
        return render(request, 'stockapp/home.html', {'AllStocks': AllStocks, 'Stocks': Data,'niftyBank': NiftyBank,'nifty50': Nifty50})

    def Broken():
        print('ubk')
        stop_event.set()  # stop the thread if websocket get disconnected

    def SendPrices(self, data):
        while not stop_event.is_set():
            channels_layer = get_channel_layer()
            NiftyBank = nse.get_index_quote("nifty bank")
            Nifty50 = nse.get_index_quote("nifty 50")
            start_time = datetime.now()
            for i in data:
                nseQuote = nse.get_quote(i)
                async_to_sync(channels_layer.group_send)(
                    'Home',
                    {
                        'type': 'stock_update',
                        'message': nseQuote,
                        'niftyBank': NiftyBank,
                        'nifty50': Nifty50
                    }
                )
            end_time = datetime.now()
            print('Duration: {}'.format(end_time - start_time))
            time.sleep(1)


class Show_Details(View):
    def get(self, request, *args, **kwargs):
        global stopevent
        Name = self.kwargs['Name']
        nseQuote = nse.get_quote(Name)
        url = f"https://www.screener.in/company/{Name}/consolidated/"
        result = requests.get(url).text
        #'<div class="sub show-more-box about" style="flex-basis: 100px">'
        soup = BeautifulSoup(result, 'lxml')
        Company_Descripton = soup.find(
            'div', {'class': "sub show-more-box about"}).get_text()
        stopevent = Event()  # for geting the current event
        # make a thread to get prices
        s = Thread(target=self.SendPrices, args=(Name,))
        s.daemon = True
        s.start()
        context = {
            'Stock': nseQuote,
            'company_description': Company_Descripton,
            'room_name': Name
        }
        return render(request, 'stockapp/Show_Page.html', context=context)

    def Broken():
        stopevent.set()  # stop the thread if websocket get disconnected

    def SendPrices(self, data):
        while not stopevent.is_set():
            channels_layer = get_channel_layer()
            nseQuote = nse.get_quote(data)
            print(nseQuote)
            async_to_sync(channels_layer.group_send)(
                str(data),
                {
                    'type': 'stock_update',
                    'message': nseQuote,
                }
            )
            time.sleep(1)
