from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', dashboard_get_usuarios_page , name="getUsuariosPage"),
    path('api/v2/admin/usuarios/insert', dashboard_usuario_insert, name="insertUsuario"),
    path('api/v2/admin/usuarios/all', dashboard_get_usuarios_all, name="getAllUsuarios"),
    path('api/v2/admin/usuarios/get', dashboard_get_user, name="getAllUsuarios"),
    
]