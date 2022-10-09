from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', getCapacitacionesPage , name="getCapacitacionesPage"),
    path('api/v2/admin/capacitaciones/insert', insertCapacitacion, name="insertCapacitacion"),
    path('api/v2/admin/capacitaciones/all', getAllCapacitaciones, name="getAllCapacitaciones"),
    path('api/v2/admin/capacitaciones/get', getCapacitacion, name="getCapacitacion"),
    path('api/v2/admin/capacitaciones/delete', dashboard_delete_capacitacion, name="deleteCapacitacion"),
]