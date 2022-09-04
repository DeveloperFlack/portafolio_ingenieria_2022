from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', getRolesPage , name="getRolesPage"),
    path('api/v2/roles/insert', insertRol, name="insertRol"),
    path('api/v2/roles/all', getAllRoles, name="getAllRoles"),
    path('api/v2/roles/get', getRol, name="getRol"),
    path('api/v2/roles/activate', enableRol, name="enableRol"),
    path('api/v2/roles/deactivate', disableRol, name="disableRol"),
    path('api/v2/roles/delete', deleteRol, name="deleteRol"),
    path('api/v2/permisos/get', getPermisos, name="getPermisos"),
    path('api/v2/permisos/insert', setPermisos, name="setPermisos"),

]

