from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', getRolesPage , name="getRolesPage"),
    path('api/v2/admin/roles/insert', insertRol, name="insertRol"),
    path('api/v2/admin/roles/all', getAllRoles, name="getAllRoles"),
    path('api/v2/admin/roles/get', getRol, name="getRol"),
    path('api/v2/admin/roles/activate', enableRol, name="enableRol"),
    path('api/v2/admin/roles/deactivate', disableRol, name="disableRol"),
    path('api/v2/admin/roles/delete', deleteRol, name="deleteRol"),
    path('api/v2/admin/permisos/get', getPermisos, name="getPermisos"),
    path('api/v2/admin/permisos/insert', setPermisos, name="setPermisos"),

]

