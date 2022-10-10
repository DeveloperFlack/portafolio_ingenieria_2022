from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', dashboard_get_usuarios_page , name="getUsuariosPage"),
    path('api/v2/admin/usuarios/insert', dashboard_usuario_insert, name="insertUsuario"),
    path('api/v2/admin/usuarios/all', dashboard_get_usuarios_all, name="getAllUsuarios"),
    path('api/v2/admin/usuarios/get', dashboard_get_user, name="getUser"),
    path('api/v2/admin/usuarios/enable', dashboard_enable_user, name="enableUser"),
    path('api/v2/admin/usuarios/disable', dashboard_disable_user, name="disableUser"),
    path('api/v2/admin/usuarios/delete', dashboard_delete_user, name="deleteUser"),
    
]