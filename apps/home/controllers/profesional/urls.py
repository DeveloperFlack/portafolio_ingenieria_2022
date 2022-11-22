from unicodedata import name
from django.urls import URLPattern, path, include
from .views import *
from apps.home.views import getHome

urlpatterns = [
    path('/', getHome , name="getHome"),
    path('portal', portal_profesional, name="profileProfesional"),
    path('portal/mis-projectos', projects_profesional, name="projectsProfesional"),
    path('portal/reportes-globales', reportes_globales_profesional, name="reportesGlobalesProfesional"),
    path('portal/reportes-globales/insert', insert_reporteglobal, name="insertReporteGlobal"),
    path('portal/reportes-globales/getAll', get_all_reportes_globales, name="getAllReportes"),
    path('portal/reportes-globales/reportes', get_reportesGlobal, name="getReportesGlobal"),
    path('portal/reportes-globales/deleteReporte', delete_reporte, name="deleteReporte"),
    path('portal/mis-tickets', tickets_profesional, name="ticketsProfesional"),
    path('api/v2/ingresar/capacitación', insert_project, name="insertCapacitacionProfesional"),
    path('api/v2/get/capacitacion', get_capacitacion, name="capacitacionProfesional"),
    path('api/v2/delete/capacitacion', delete_capacitacion, name="deleteCapacitacionProfesional"),
    path('api/v2/get/actividad-profesional', getActividadProfesional, name="getActividadProfesional"),
    path('api/v2/get/portal/mis-projectos/actividades', getAllActividadProfesional, name="getAllActividadProfesional"),
    path('api/v2/capacitaciones/enableActividadProfesional', enableActividadProfesional, name="enableActividadProfesional"),
    path('api/v2/capacitaciones/disableActividadProfesional', disableActividadProfesional, name="disableActividadProfesional"),
    path('api/v2/generate/pdf', reportePdf, name="reportePdf"),


]

