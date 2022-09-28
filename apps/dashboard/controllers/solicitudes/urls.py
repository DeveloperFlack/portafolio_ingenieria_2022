from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', dashboard_get_solicitudes_page , name="getSolicitudesPage"),
    path('admin/api/v2/solicitudes/all', dashboard_get_all_solicitudes, name="getAllSolicitudes"),
    path('admin/api/v2/solicitudes/get', getSolicitud, name="getSolicitud"),
    path('admin/api/v2/solicitudes/update', updateSolicitud, name="updateSolicitud"),

]