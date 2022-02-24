from ast import Break, arg
import re
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.shortcuts import render
import schedule
import time
from threading import Thread
import requests
from nsetools import Nse
from threading import Thread , Event
nse = Nse()
from bs4 import BeautifulSoup
from channels.layers import get_channel_layer
from django.views import View
# Create your views here.
def Home(request):
    AllStocks= nse.get_stock_codes()
    return render(request,'stockapp/home.html',{'Stocks': AllStocks})

class Show_Details(View):
    def get(self,request,*args,**kwargs):
        global stop_event
        Name =self.kwargs['Name']
        nseQuote = nse.get_quote(Name)
        url = f"https://www.screener.in/company/{Name}/consolidated/"
        result = requests.get(url).text
        #'<div class="sub show-more-box about" style="flex-basis: 100px">'
        soup = BeautifulSoup(result,'lxml')
        Company_Descripton=soup.find('div', {'class':"sub show-more-box about"}).get_text()
        stop_event= Event() #for geting the current event
        s=Thread(target=self.SendPrices,args=(Name,)) #make a thread to get prices
        s.daemon=True
        s.start()
        context = {
            'Stock':nseQuote,
            'company_description':Company_Descripton,
            'room_name': Name
        }
        return render(request,'stockapp/Show_Page.html',context=context)
    def Broken():
        stop_event.set() # stop the thread if websocket get disconnected 
    def SendPrices(self,data):
        while not stop_event.is_set():
            time.sleep(10) 
            channels_layer = get_channel_layer()
            nseQuote= nse.get_quote(data)
            print(nseQuote)
            async_to_sync(channels_layer.group_send)(
            str(data),
                {
                'type': 'stock_update',
                'message': nseQuote,
                }
            )