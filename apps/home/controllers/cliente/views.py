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
    if (sessionStatus['cliente'] == False ):
        return redirect('index')
    
    data = {
        'table' : getSolicitudes(request)
    }
    
    return render(request, 'profile-cliente.html', data)

def registerCliente(request):
    if request.method == "POST":
        v_rut_cliente = request.POST.get("txtRutCliente")
        exist = fc_get_cliente(v_rut_cliente)
        if (exist == ()):
            # INSERTAR CLIENTE
            v_rut_empresa = request.POST.get("txtRutEmpresa")
            v_n1_cliente = request.POST.get("txtN1Cliente")
            v_n2_cliente = request.POST.get("txtN2Cliente")
            v_ap_cliente = request.POST.get("txtApellidoPaternoCliente")
            v_am_cliente = request.POST.get("txtApellidoMaternoCliente")
            v_correo_cliente = request.POST.get("txtCorreoCliente")
            v_contacto_cliente = request.POST.get("txtContactoCliente")
            v_nombre_empresa = request.POST.get("txtNombreEmpresa")
            vaa = request.POST.get("txtPasswordCliente")

            v_password_cliente = hashlib.sha256(vaa.encode('utf-8')).hexdigest()
            
            v_id_rol = 2
            v_status_cliente = 1

            fc_home_register(
                v_rut_cliente, v_password_cliente, v_n1_cliente, v_n2_cliente, v_ap_cliente, v_am_cliente, 
                v_correo_cliente, v_contacto_cliente, v_rut_empresa, v_nombre_empresa, v_id_rol, v_status_cliente
            )
            # print (urls.urlpatterns[0])
            return redirect("getHome")

        else:
            # ACTUALIZAR CLIENTE
            exist = fc_get_cliente(v_rut_cliente)
            if (exist != ()):
                v_rut_empresa = request.POST.get("txtRutEmpresa")
                v_n1_cliente = request.POST.get("txtN1Cliente")
                v_n2_cliente = request.POST.get("txtN2Cliente")
                v_ap_cliente = request.POST.get("txtApellidoPaternoCliente")
                v_am_cliente = request.POST.get("txtApellidoMaternoCliente")
                v_correo_cliente = request.POST.get("txtCorreoCliente")
                v_contacto_cliente = request.POST.get("txtContactoCliente")
                v_rut_empresa = request.POST.get("txtRutEmpresa")
                v_nombre_empresa = request.POST.get("txtNombreEmpresa")
                vaa = request.POST.get("txtPasswordCliente")
                
                v_password_cliente = hashlib.sha256(vaa.encode('utf-8')).hexdigest()

                v_id_rol = 2
                v_status_cliente = 1

                #fc_update_cliente(v_rut_empresa, v_nombre_empresa, v_n1_cliente, v_n2_cliente, v_ap_cliente, v_am_cliente, v_rut_cliente, v_contacto_cliente, v_correo_cliente, v_password_cliente, v_id_rol, v_status_cliente)
                return redirect("getHome")
            else:
                return redirect("getHome")
    else:
        return redirect("getHome")

def solicitudInsert(request):
    status = request_session(request)
    if (status == False):
        return redirect('getHome')
    
    if request.method == "POST":  
        # INSERTAR USUARIO HOME (CLIENTE)
        v_rut_cliente = request.session['cliente']['rut_cliente']
        # v_rut_cliente = "19934512-5"
        v_id_capacitacion = request.POST.get("selectNombreSolicitud")
        v_nombre_solicitud = request.POST.get("txtNombreSolicitud")
        v_descripcion_solicitud = request.POST.get("txtDescripcionSolicitud")
        v_tipo_solicitud = request.POST.get("selectTipoSolicitud")
        v_estado_solicitud = 1
        v_status_solicitud = 1

        fc_solicitud_insert(v_rut_cliente, v_id_capacitacion, v_nombre_solicitud, v_descripcion_solicitud, v_tipo_solicitud, v_estado_solicitud, v_status_solicitud)

        #print (urls.urlpatterns[0])
        return redirect("profileCliente")
    else:
        return redirect("profileCliente")

def getSolicitud(request):
    session_check = 'cliente' in request.session
    if (session_check == True):
        v_rut_cliente = request.session['cliente']['rut_cliente']
        data_solicitudes = fc_get_solicitudes(v_rut_cliente)
        print (data_solicitudes)
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

