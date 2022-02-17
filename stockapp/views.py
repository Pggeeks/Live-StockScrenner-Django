from asyncio import tasks
from concurrent.futures import thread
import time
from tokenize import Name
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.shortcuts import render  , HttpResponse
from django.template import context
import queue
from threading import Thread
import requests
from nsetools import Nse
import json
from threading import Thread
import schedule
nse = Nse()
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from django.views import View
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def Home(request):
    AllStocks= nse.get_stock_codes()
    return render(request,'stockapp/home.html',{'Stocks': AllStocks})
class Show_Details(View):
    def get(self,request,*args,**kwargs):
        Name =self.kwargs['Name']
        nseQuote = nse.get_quote(Name)
        url = f"https://www.screener.in/company/{Name}/consolidated/"
        result = requests.get(url).text
        #'<div class="sub show-more-box about" style="flex-basis: 100px">'
        soup = BeautifulSoup(result,'lxml')
        Company_Descripton=soup.find('div', {'class':"sub show-more-box about"}).get_text()
        print(nseQuote)
        context = {
            'Stock':nseQuote,
            'company_description':Company_Descripton,
            'room_name': Name
        }
        return render(request,'stockapp/Show_Page.html',context=context)

    ## FOR AJAX REQUEST SENDS STOCK DATA
    def post(self,request,*args,**kwargs):
        data=request.POST.get('data')
        print(data)
        s=Thread(target=self.SendPrices,args=(data,))
        s.daemon=True
        s.start()
        return HttpResponse(data)
        
    def SendPrices(self,data):
        print('send')
        channels_layer = get_channel_layer()
        while True:
            time.sleep(5)
            nseQuote= nse.get_quote(data)
            async_to_sync(channels_layer.group_send)(
            str(data),
                {
                'type': 'stock_update',
                'message': nseQuote,
                }
            )