from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', getSolicitudesPage , name="getSolicitudesPage"),
    path('api/v2/solicitudes/all', getAllSolicitudes, name="getAllSolicitudes"),
    path('api/v2/solicitudes/get', getSolicitud, name="getSolicitud"),
    path('update/solicitud', updateSolicitud, name="updateSolicitud"),

]