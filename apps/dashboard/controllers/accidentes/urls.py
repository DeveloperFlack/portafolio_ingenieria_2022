from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', getAccidentesPage , name="getAccidentesPage"),
    path('api/v2/admin/accidentes/get', get_accidentes, name="getAccidentes"),
    path('api/v2/admin/accidentes/all', getAllAccidentes, name="getAllAccidentes"),
    path('api/v2/admin/accidentes/delete', delete_accidentes, name="deleteAccidente"),
    path('api/v2/admin/accidentes/enable', enable_accidente, name="enableAccidente"),
    path('api/v2/admin/accidentes/disable', disable_accidente, name="disableAccidente"),

]