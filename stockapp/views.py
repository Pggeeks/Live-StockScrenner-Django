from asyncio import tasks
from concurrent.futures import thread
import time
from tokenize import Name
from asgiref.sync import async_to_sync
from django.shortcuts import render  , HttpResponse
from django.template import context
import queue
from threading import Thread
import requests
from nsetools import Nse
nse = Nse()
import json
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from django.views import View
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
        currentprice = nseQuote['lastPrice']
        context = {
            'Stock':nseQuote,
            'company_description':Company_Descripton,
            'room_name': 'StockDetails'
        }
        return render(request,'stockapp/Show_Page.html',context=context)
# async def update()