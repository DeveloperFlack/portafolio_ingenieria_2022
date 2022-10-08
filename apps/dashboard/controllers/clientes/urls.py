from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', getClientesPage , name="getClientesPage"),
    path('api/v2/admin/clientes/all', getAllClientes , name="getAllClientes")
]