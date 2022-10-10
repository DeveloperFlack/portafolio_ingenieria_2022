from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', getClientesPage , name="getClientesPage"),
    path('api/v2/admin/clientes/all', getAllClientes , name="getAllClientes"),
    path('api/v2/admin/clientes/get', dashboard_get_cliente , name="getCliente"),
    path('api/v2/admin/clientes/update', dashboard_update_cliente , name="updateCliente"),
]