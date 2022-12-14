from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', getCapacitacionesPage , name="getCapacitacionesPage"),
    path('api/v2/admin/capacitaciones/insert', insertCapacitacion, name="insertCapacitacion"),
    path('api/v2/admin/capacitaciones/all', getAllCapacitaciones, name="getAllCapacitaciones"),
    path('api/v2/admin/capacitaciones/get', getCapacitacion, name="getCapacitacion"),
    path('api/v2/admin/capacitaciones/enable', dashoard_enable_capacitacion, name="enableCapacitacion"),
    path('api/v2/admin/capacitaciones/disable', dashoard_disable_capacitacion, name="disableCapacitacion"),
    path('api/v2/admin/capacitaciones/delete', dashboard_delete_capacitacion, name="deleteCapacitacion"),
    path('api/v2/admin/capacitaciones/insertActividad', dashboard_insert_actividades, name="InsertActividades"),
    path('api/v2/admin/capacitaciones/getActividad', getActividad, name="getActividad"),
]