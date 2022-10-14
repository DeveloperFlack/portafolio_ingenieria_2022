from genericpath import exists
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
import pymysql
import hashlib
from apps.dashboard.controllers.roles.usp import fc_get_permisos
from django.contrib import messages
from apps.helpers import request_session

def getAccidentesPage(request):
    data = {
        'id' : 8,
        'meta_title': 'Dashboard - Accidentes',
        'breadcrumb': "Accidentes",
        'title': 'Lista de Accidentes',
        'subtitle': 'Lista completa de Accidentes',
        'button_add': 'Añadir Accidentes',
    }
    return render(request, "accidentes.html", data)


# INSERTAR ACCIDENTES
def insertar_accidentes(request):
    if(request.method == 'POST'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                id_accidente = request.POST.get("idAccidentes")
                cursor.execute("SELECT * FROM nma_accidentes WHERE id_accidente = %s" % (id_accidente))
                exist = cursor.fetchall()
                
                if (exist != ()):
                    v_nombre_accidente = request.POST.get("NombreAccidente")
                    v_descripcion_accidente = request.POST.get("DescripcionAccidente")
                    v_fecha_accidente = request.POST.get("FechaAccidente")
                    v_hora_accidente = request.POST.get("HoraAccidente")
                    v_tipo_accidente = request.POST.get("TipoAccidente")
                    v_status_accidente = request.POST.get("Status_Accidente")
                    cursor.execute('INSERT INTO nma_capacitacion (nombre_accidente,descripcion_accidente,fecha_accidente,hora_accidente,tipo_accidente,status_accidente), VALUES (%s,"%s","%s",%s,"%s",%s)' % (v_nombre_accidente,v_descripcion_accidente,v_fecha_accidente,v_hora_accidente,v_tipo_accidente,v_status_accidente))
                    cx.commit()
            cx.close()
            return "Realizado con Éxito"
        except Exception as ex:
            print(ex)
            return "Error en el Proceso"
    else:
        return redirect("profileCliente")
