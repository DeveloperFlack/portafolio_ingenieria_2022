from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', getClientesPage , name="getClientesPage"),
    path('ListarClientes', getAllClientes , name="getAllClientes")
]