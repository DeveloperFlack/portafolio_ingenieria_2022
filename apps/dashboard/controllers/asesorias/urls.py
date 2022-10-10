from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', getAsesoriasPage , name="getAsesoriasPage"),
    path('api/v2/admin/asesorias/insert', insertAsesoria, name="insertAsesoria"),
    path('api/v2/admin/asesorias/all', getALLAsesorias, name="getAllAsesoria"),
    path('api/v2/admin/asesorias/get', getAsesoria, name="getAsesoria"),
    path('api/v2/admin/asesorias/delete', dashboard_delete_asesoria, name="deleteAsesoria"),
    path('api/v2/admin/asesorias/enable', dashboard_enable_asesoria, name="enableAsesoria"),
    path('api/v2/admin/asesorias/disable', dashoard_disable_asesoria, name="disableAsesoria"),

]