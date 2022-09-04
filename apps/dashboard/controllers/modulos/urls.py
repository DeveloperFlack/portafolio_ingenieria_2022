from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', getModulosPage , name="getModulosPage"),
    path('api/v2/modulos/insert', insertModulo, name="insertModulo"),
    path('api/v2/modulos/all', getAllModulos, name="getAllModulos"),
    path('api/v2/modulos/get', getModulo, name="getModulo"),
    path('api/v2/modulos/activate', enableModulo, name="enableModulo"),
    path('api/v2/modulos/deactivate', disableModulo, name="disableModulo"),
    path('api/v2/modulos/delete', deleteModulo, name="deleteModulo"),
]

