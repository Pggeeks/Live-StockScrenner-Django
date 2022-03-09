from django.contrib import admin
from django.urls import path
from django.urls.conf import include ,re_path
import stockapp
from . import views
urlpatterns = [
    path('',views.Home.as_view(),name='Home'),
    path(r'stock/<str:Name>',views.Show_Details.as_view()),
]
 