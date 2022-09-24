from unicodedata import name
from django.urls import URLPattern, path, include
from .views import *
from apps.home.views import getHome


urlpatterns = [
    path('/', getHome , name="getHome"),
    path('api/v2/register', registerCliente , name="registerCliente"),
    path('api/v2/login', loginCliente , name="loginCliente"),
    path('logout', logoutCliente, name="logoutCliente"),
    path('profile', profileCliente, name="profileCliente"),
    path('profile/send/solicitud', solicitudInsert, name="solicitudInsert"),
]
