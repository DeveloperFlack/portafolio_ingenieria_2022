from unicodedata import name
from django.urls import URLPattern, path, include
from .views import *
from apps.home.views import getHome

urlpatterns = [
    path('/', getHome , name="getHome"),
    path('portal', portal_profesional, name="profileProfesional"),
    path('portal/mis-projectos', projects_profesional, name="projectsProfesional"),
    path('portal/mis-tickets', tickets_profesional, name="ticketsProfesional"),
    path('api/v2/ingresar/capacitación', insert_project, name="insertCapacitacion"),
    
]

