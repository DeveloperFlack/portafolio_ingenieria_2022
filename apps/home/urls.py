from unicodedata import name
from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', getHome , name="index"),
    path('profesional/', include("apps.home.controllers.profesional.urls")),
    path('cliente/', include("apps.home.controllers.cliente.urls")),
]

