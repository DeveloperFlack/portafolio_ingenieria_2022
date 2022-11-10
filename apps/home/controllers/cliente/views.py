from genericpath import exists
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .usp import *
from apps.dashboard.controllers.roles.usp import fc_get_permisos
from django.contrib import messages
from apps.helpers import request_session
from .service import payService
import requests



def profileCliente(request):
    sessionStatus = request_session(request)
    if (sessionStatus['cliente'] != True ):
        return redirect('index')
        
    
    data = {
        'session_status' : request_session(request),
        'capacitaciones' :  get_capacitaciones(request),
        'table' : getSolicitud(request),
        'tableAcc': getAccidente(request),
        'asesorias' : get_asesorias(request),
        'accidente' : get_reportarAccidente(request),
        'cliente' : getInformacion(request)
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
        # return redirect("profileCliente")
        url = request.build_absolute_uri()
        url = url.split('/')
        
        params={'numberCapacitacion' : v_id_capacitacion }
        #return requests(,url[0] + '//' + url[2] + '/cliente/profile/pay/cart', params={'numberCapacitacion' : v_id_capacitacion, 'request' : request})
        return payService(request, params)
    else:
        messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo')
        return redirect("profileCliente")

def getInformacion(request):
    v_rut_cliente = request.session['cliente']['rut_cliente']
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("SELECT * FROM nma_cliente WHERE rut_cliente = '%s'" % v_rut_cliente) 
            datos = cursor.fetchall()
            data_to_array = []
            for i in range(len(datos)):
                data_to_array.append({
                    "rut_cliente" : datos[i][0],
                    "n1_cliente" : datos[i][2],
                    "ap_cliente" : datos[i][4],
                    "nombre_empresa" : datos[i][9],
                    "rut_empresa_cliente" : datos[i][8],
                    "correo_cliente" : datos[i][6],
                })           
            return data_to_array
    except Exception as ex:
        print (ex)

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

## TABLA ACCIDENTES CLIENTE
def getAccidente(request):
    session_check = 'cliente' in request.session
    if (session_check == True):
        v_rut_cliente = request.session['cliente']['rut_cliente']
        data_accidentes = fc_get_accidentes(v_rut_cliente)
        # print (data_solicitudes)
        data_to_array = []
        if (data_accidentes != ()):
            for i in data_accidentes:
                data_to_array.append({
                    "nombre_accidente": i[2],
                    "descripcion_accidente" : i[3],
                    "fecha_accidente": i[4],
                    "hora_accidente": i[5],
                    "tipo_accidente": i[6],
                })
            data_table = {'tableAcc' : ""}
            for ax in range(len(data_to_array)):
                v_nombre_accidente = data_to_array[ax]["nombre_accidente"]
                v_descripcion_accidente = data_to_array[ax]['descripcion_accidente']
                v_fecha_accidente = data_to_array[ax]['fecha_accidente']
                v_hora_accidente = data_to_array[ax]['hora_accidente']
                v_tipo_accidente = data_to_array[ax]['tipo_accidente']
                data_table['tableAcc'] += """
                    <tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                    </tr>
                """ % (v_nombre_accidente, v_descripcion_accidente, v_fecha_accidente, v_hora_accidente, v_tipo_accidente)
            return data_table['tableAcc']
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
                    "descripcion_accidente" : accidente[i][3],
                    "fecha_accidente" : accidente[i][4],
                    "hora_accidente" : accidente[i][5],
                    "tipo_accidente" : accidente[i][6]

                })
            
            return data_to_array
    except Exception as ex:
        print (ex)

# INSERTAR ACCIDENTES CLIENTE
def insertAccidentesCliente(request):
    if(request.method == 'POST'):
        v_id_accidente = request.POST.get('idAccidenteCliente')
        v_rut_cliente = request.session['cliente']['rut_cliente']
        try:
            cx = get_connection()
            with cx.cursor() as cursor:

                cursor.execute("SELECT * FROM nma_accidentes WHERE id_accidente = '%s'" % (v_id_accidente))
                exists = cursor.fetchall()

                print(exists)

                if (exists == ()):
                    v_nombre_accidente = request.POST.get("txtNombreAccidenteCliente")
                    v_descripcion_accidente = request.POST.get("txtDescripcionAccidenteCliente")
                    v_fecha_accidente = request.POST.get("txtFechaAccidenteCliente")
                    v_hora_accidente = request.POST.get("txtHoraAccidenteCliente")
                    v_tipo_accidente = request.POST.get("txtTipoAccidenteCliente")
                    v_status_accidente = 1
                    cursor.execute("""INSERT INTO nma_accidentes 
                    (rut_cliente, nombre_accidente, descripcion_accidente, fecha_accidente, hora_accidente, tipo_accidente, status_accidente)
                    VALUES ("%s", "%s", "%s", "%s", "%s", "%s", %s)"""
                    % (v_rut_cliente, v_nombre_accidente, v_descripcion_accidente, v_fecha_accidente, v_hora_accidente, v_tipo_accidente, v_status_accidente))
                    cx.commit()

                else:
                    v_nombre_accidente = request.POST.get("txtNombreAccidenteCliente")
                    v_descripcion_accidente = request.POST.get("txtDescripcionAccidenteCliente")
                    v_fecha_accidente = request.POST.get("txtFechaAccidenteCliente")
                    v_hora_accidente = request.POST.get("txtHoraAccidenteCliente")
                    v_tipo_accidente = request.POST.get("txtTipoAccidenteCliente")
                    v_status_accidente = 1
                    cursor.execute("""UPDATE nma_accidentes SET nombre_accidente = "%s",
                    descripcion_accidente = "%s", fecha_accidente = "%s", hora_accidente = "%s", 
                    tipo_accidente = "%s", status_accidente = %s WHERE (id_accidente = %s)""" 
                    % (v_nombre_accidente, v_descripcion_accidente, v_fecha_accidente, v_hora_accidente, v_tipo_accidente, v_status_accidente, v_id_accidente))
                    cx.commit()

            cx.close()
            return redirect("profileCliente")
        except Exception as ex:
            print(ex)
            return redirect("profileCliente")
    else:
        return redirect("profileCliente")