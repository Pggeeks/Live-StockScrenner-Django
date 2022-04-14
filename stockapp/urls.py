from django.urls import path
from . import views
urlpatterns = [
    path('',views.Home.as_view(),name='Home'),
    path(r'stock/<str:Name>',views.Show_Details.as_view()),
    path('ajax/get-info',views.get_info),
    path('ajax/get-nifty',views.get_nifty),
    path('ajax/get-topstocks',views.get_topstocks),
    path('stock/ajax/Get-SelectedStock/',views.Get_SelectedStock),
]
