from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', dashboard_get_solicitudes_page , name="getSolicitudesPage"),
    path('api/v2/admin/solicitudes/all', dashboard_get_all_solicitudes, name="getAllSolicitudes"),
    path('api/v2/admin/solicitudes/get', dashboard_get_solicitud, name="getSolicitud"),
    path('api/v2/admin/solicitudes/update', dashboard_update_solicitud, name="updateSolicitud"),
    path('api/v2/admin/solicitudes/delete', dashboard_delete_solicitud, name="deleteSolicitud"),
    path('api/v2/admin/solicitudes/enable', dashboard_enable_solicitud, name="enableSolicitud"),
    path('api/v2/admin/solicitudes/disable', dashboard_disable_solicitud, name="disableSolicitud"),

]