from unicodedata import name
from django.urls import URLPattern, path, include
from .views import *
from apps.home.views import getHome


urlpatterns = [
    path('/', getHome , name="getHome"),
    path('profile', profileCliente, name="profileCliente"),
    path('profile/send/solicitud', solicitudInsert, name="solicitudInsert"),
]
