import time
from threading import Event, Thread

import requests
from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup
from channels.layers import get_channel_layer
from django.shortcuts import render
from django.views import View
from nsetools import Nse

nse = Nse()


class Home(View):
    def get(self, request):
        global stop_event
        AllStocks = nse.get_stock_codes()
        a = {"RELIANCE": "RELIANCE INDUSTRIES", "HDFCBANK": "HDFC BANK", "INFY": "INFOSYS",
             "ICICIBANK": "ICICI BANK", "TCS": "TATA CONSULTANCY SERVICES", "LT": "LARSEN & TOUBRO LTD"}
        Data = [nse.get_quote(i) for i in a]
        Nifty50 = nse.get_index_quote("nifty 50")
        NiftyBank = nse.get_index_quote("nifty Bank")
        stop_event = Event()  # for geting the current event
        # make a thread to get prices
        s = Thread(target=self.SendPrices, args=(a,))
        s.daemon = True
        s.start()
        return render(request, 'stockapp/home.html', {'AllStocks': AllStocks, 'Stocks': Data, 'niftyBank': NiftyBank, 'nifty50': Nifty50})

    def Broken():
        # stop_event.clear()
        stop_event.set()  # stop the thread if websocket get disconnected

    def clearevent():
        stop_event.clear()

    def SendPrices(self, data):
        while not stop_event.is_set():
            channels_layer = get_channel_layer()
            NiftyBank = nse.get_index_quote("nifty bank")
            Nifty50 = nse.get_index_quote("nifty 50")
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
            time.sleep(7)


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
        # stop_event.clear()
        stopevent.set()  # stop the thread if websocket get disconnected

    def clearevent():
        stopevent.clear()

    def SendPrices(self, data):
        while not stopevent.is_set():
            channels_layer = get_channel_layer()
            nseQuote = nse.get_quote(data)
            async_to_sync(channels_layer.group_send)(
                str(data).upper(),
                {
                    'type': 'stock_update',
                    'message': nseQuote,
                }
            )
            time.sleep(7)
