from genericpath import exists
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .usp import *
import pymysql
import hashlib
from apps.dashboard.controllers.roles.usp import fc_get_permisos
from django.contrib import messages
from apps.helpers import request_session

def profileCliente(request):
    sessionStatus = request_session(request)
    if (sessionStatus['cliente'] != True ):
        return redirect('index')
        
    
    data = {
        'session_status' : request_session(request),
        'capacitaciones' :  get_capacitaciones(request),
        'table' : getSolicitud(request),
        'asesorias' : get_asesorias(request),
        'accidente' : get_reportarAccidente(request)
    }
    
    return render(request, 'profile-cliente.html', data)

def solicitudInsert(request):
    status = request_session(request)
    if (status == False):
        return redirect('getHome')
    
    if request.method == "POST":  
        # INSERTAR USUARIO HOME (CLIENTE)
        v_rut_cliente = request.session['cliente']['rut_cliente']
        v_id_capacitacion = request.POST.get("selectNombreSolicitud")
        v_nombre_solicitud = request.POST.get("txtNombreSolicitud")
        v_descripcion_solicitud = request.POST.get("txtDescripcionSolicitud")
        v_tipo_solicitud = request.POST.get("selectTipoSolicitud")
        v_estado_solicitud = 0
        v_status_solicitud = 1

        fc_solicitud_insert(v_rut_cliente, v_id_capacitacion, v_nombre_solicitud, v_descripcion_solicitud, v_tipo_solicitud, v_estado_solicitud, v_status_solicitud)

        # print (urls.urlpatterns[0])
        return redirect("profileCliente")
    else:
        messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo')
        return redirect("profileCliente")

def getSolicitud(request):
    session_check = 'cliente' in request.session
    if (session_check == True):
        v_rut_cliente = request.session['cliente']['rut_cliente']
        data_solicitudes = fc_get_solicitudes(v_rut_cliente)
        # print (data_solicitudes)
        data_to_array = []
        if (data_solicitudes != ()):
            for x in data_solicitudes:
                data_to_array.append({
                    "nombre_solicitud": x[4],
                    "descripcion_solicitud": x[5],
                    "fecha": x[7],
                    "time_start": x[8],
                    "time_end": x[9],
                })
            data_table = {'table' : ""}
            for ax in range(len(data_to_array)):
                v_nombre_solicitud = data_to_array[ax]["nombre_solicitud"]
                v_descripcion_solicitud = data_to_array[ax]['descripcion_solicitud']
                v_fecha = data_to_array[ax]['fecha']
                v_time_start = data_to_array[ax]['time_start']
                v_time_end = data_to_array[ax]['time_end']
                data_table['table'] += """ 
                    <tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                    </tr>
                """ % (v_nombre_solicitud, v_descripcion_solicitud, v_fecha, v_time_start, v_time_end)
            return data_table['table']
        else:
            return redirect("profileCliente")
    else:
        return redirect("profileCliente")

def get_capacitaciones(request):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute('SELECT * FROM nma_capacitacion WHERE status_capacitaciones != 0')
            capacitacion = cursor.fetchall()
            data_to_array = []
            
            for i in range(len(capacitacion)):
                data_to_array.append({
                    "id_capacitacion" : capacitacion[i][0],
                    "nombre_capacitacion" : capacitacion[i][2],
                })
            
            return data_to_array
    except Exception as ex:
        print (ex)

def get_asesorias(request):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute('SELECT * FROM nma_asesoria WHERE status_asesoria != 0')
            asesoria = cursor.fetchall()
            data_to_array = []
            
            for i in range(len(asesoria)):
                data_to_array.append({
                    "id_asesoria" : asesoria[i][0],
                    "nombre_asesoria" : asesoria[i][2],
                })
            
            return data_to_array
    except Exception as ex:
        print (ex)

def get_reportarAccidente(request):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute('SELECT * FROM nma_accidentes WHERE status_accidente != 0')
            accidente = cursor.fetchall()
            data_to_array = []
            
            for i in range(len(accidente)):
                data_to_array.append({
                    "id_accidente" : accidente[i][0],
                    "nombre_accidente" : accidente[i][2],
                })
            
            return data_to_array
    except Exception as ex:
        print (ex)