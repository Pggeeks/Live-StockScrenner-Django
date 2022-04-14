import json
import time
from threading import Event, Thread

from django.http import JsonResponse
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
        a = {"RELIANCE": "RELIANCE INDUSTRIES", "HDFCBANK": "HDFC BANK", "INFY": "INFOSYS",
             "ICICIBANK": "ICICI BANK", "TCS": "TATA CONSULTANCY SERVICES", "LT": "LARSEN & TOUBRO LTD"}
        stop_event = Event()  # for geting the current event
        # make a thread to get prices
        s = Thread(target=self.SendPrices, args=(a,))
        s.daemon = True
        s.start()
        return render(request, 'stockapp/home.html')

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
            print('iiiiiiiiiii')
            print(NiftyBank)
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
        stopevent = Event()  # for geting the current event
        # make a thread to get prices
        s = Thread(target=self.SendPrices, args=(Name,))
        s.daemon = True
        s.start()
        context = {
            'Name': Name
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

#### ajax views for home 
def get_info(data):
    print('ajax1',data)
    AllStocks = nse.get_stock_codes()
    return JsonResponse(AllStocks,safe=False,encoder=json.JSONEncoder)
def get_nifty(data):
    print('ajax2',data)
    # nifty={'nifty 50':'NIFTY_50','nifty Bank':'BANKNIFTY'}
    # Data = [nse.get_index_quote(i) for i in nifty]
    NiftyBank = nse.get_index_quote("nifty bank")
    Nifty50 = nse.get_index_quote("nifty 50")
    Data={'niftyBank': NiftyBank,
    'nifty50': Nifty50}
    return JsonResponse(Data,safe=False,encoder=json.JSONEncoder)
def get_topstocks(data):
    a = {"RELIANCE": "RELIANCE INDUSTRIES", "HDFCBANK": "HDFC BANK", "INFY": "INFOSYS",
             "ICICIBANK": "ICICI BANK", "TCS": "TATA CONSULTANCY SERVICES", "LT": "LARSEN & TOUBRO LTD"}
    Data = [nse.get_quote(i) for i in a]
    return JsonResponse(Data,safe=False,encoder=json.JSONEncoder)

def Get_SelectedStock(request):
    Name = request.POST.get('Name')
    nseQuote = nse.get_quote(Name)
    url = f"https://www.screener.in/company/{Name}/consolidated/"
    result = requests.get(url).text
        # '<div class="sub show-more-box about" style="flex-basis: 100px">'
    soup = BeautifulSoup(result, 'lxml')
    Company_Descripton = soup.find(
        'div', {'class': "sub show-more-box about"}).get_text()
    return JsonResponse(Company_Descripton,safe=False,encoder=json.JSONEncoder)