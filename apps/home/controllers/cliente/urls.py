from unicodedata import name
from django.urls import URLPattern, path, include
from .views import *
from apps.home.views import getHome
from apps.home.controllers.cliente.service import *


urlpatterns = [
    path('/', getHome , name="getHome"),
    path('profile', profileCliente, name="profileCliente"),
    path('confirm-pay', afterPayService, name="afterPayService"),
    path('profile/send/solicitud', solicitudInsert, name="solicitudInsert"),
    path('profile/send/accidente', insertAccidentesCliente, name="reportarAccidente"),
    path('profile/pay/cart', payService, name="payService"),
    
]
