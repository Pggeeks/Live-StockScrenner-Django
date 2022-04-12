from urllib import response
from celery import shared_task
from time import sleep, time

from django.http import HttpResponse, JsonResponse
@shared_task
def file_transfer(password):
   sleep(password)
   print(password)