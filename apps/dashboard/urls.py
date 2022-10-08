from unicodedata import name
from django.urls import URLPattern, path, include
from .views import *

urlpatterns = [
    path('', getDashboard , name="principalDashboard"),
    path('modulos/', include("apps.dashboard.controllers.modulos.urls")),
    path('usuarios/', include("apps.dashboard.controllers.usuarios.urls")),
    path('clientes/', include("apps.dashboard.controllers.clientes.urls")),
    path('roles/', include("apps.dashboard.controllers.roles.urls")),
    path('solicitudes/', include("apps.dashboard.controllers.solicitudes.urls")),
    path('login/', loginDashboard, name="loginDashboard"),
    path('login/auth/', loginAdministrador, name="loginAdministrador"),
    path('logout/', logoutAdm, name="logoutAdm"),

]

