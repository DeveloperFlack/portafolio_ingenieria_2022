from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', getUsuariosPage , name="getUsuariosPage"),
    path('api/v2/usuarios/insert', insertUsuario, name="insertUsuario"),
    path('api/v2/usuarios/all', getAllUsuarios, name="getAllUsuarios"),
]