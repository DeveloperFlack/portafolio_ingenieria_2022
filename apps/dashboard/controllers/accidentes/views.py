from genericpath import exists
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
import pymysql
import hashlib
from apps.dashboard.usp import get_connection
from .views import *
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
def insertAccidentes(request):
    if(request.method == 'POST'):
        v_id_accidente = request.POST.get("idAccidente")
        if (v_id_accidente == ""):
            v_id_accidente = 0
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute("SELECT * FROM nma_accidentes WHERE id_accidente = %s" % (v_id_accidente))
                exist = cursor.fetchall()

                if (exist == ()):
                    v_nombre_accidente = request.POST.get("txtNombreAccidente")
                    v_descripcion_accidente = request.POST.get("txtDescripcionAccidente")
                    v_fecha_accidente = request.POST.get("txtFechaAccidente")
                    v_hora_accidente = request.POST.get("txtHoraAccidente")
                    v_tipo_accidente = request.POST.get("txtTipoAccidente")
                    v_status_accidente = 0
                    cursor.execute('''INSERT INTO nma_accidentes 
                    (nombre_accidente, descripcion_accidente, fecha_accidente, hora_accidente, tipo_accidente, status_accidente)
                    VALUES ("%s", "%s", "%s", "%s", "%s", %s)'''
                    % (v_nombre_accidente, v_descripcion_accidente, v_fecha_accidente, v_hora_accidente, v_tipo_accidente, v_status_accidente))
                    cx.commit()
                else:
                    v_nombre_accidente = request.POST.get("txtNombreAccidente")
                    v_descripcion_accidente = request.POST.get("txtDescripcionAccidente")
                    v_fecha_accidente = request.POST.get("txtFechaAccidente")
                    v_hora_accidente = request.POST.get("txtHoraAccidente")
                    v_tipo_accidente = request.POST.get("txtTipoAccidente")
                    v_status_accidente = 0
                    cursor.execute(''' UPDATE nma_accidentes SET nombre_accidente = "%s",
                    descripcion_accidente = "%s", fecha_accidente = "%s", hora_accidente = "%s", 
                    tipo_accidente = "%s", status_accidente = %s WHERE (id_accidente = %s)''' 
                    % (v_nombre_accidente, v_descripcion_accidente, v_fecha_accidente, v_hora_accidente, v_tipo_accidente, v_status_accidente))
                    cx.commit()

            cx.close()
            return redirect("getAccidentesPage")
        except Exception as ex:
            print(ex)
            return redirect("getAccidentesPage")
    else:
        return redirect("getAccidentesPage")

def disable_accidente(request):
    if (request.method == 'GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_accidente = request.GET.get('idAccidente')
                cursor.execute("SELECT * FROM nma_accidentes WHERE id_accidente = %s" % (v_id_accidente))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("UPDATE nma_accidentes SET status_accidente = 0 WHERE id_accidente = %s" % (v_id_accidente))
                    cx.commit()
                    messages.add_message(request, messages.SUCCESS, 'Accidente Desactivado exitosamente!')
                    return redirect("getAccidentesPage")
                else:
                    messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
                    return redirect("getAccidentesPage")
        except Exception as ex:
            print(ex)
            return redirect("getAccidentesPage")
    else:
        return redirect("getAccidentesPage")

def enable_accidente(request):
    if (request.method == 'GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_accidente = request.GET.get('idAccidente')
                cursor.execute("SELECT * FROM nma_accidente WHERE id_accidente = %s" % (v_id_accidente))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("UPDATE nma_accidentes SET status_accidente = 1 WHERE id_accidente = %s" % (v_id_accidente))
                    cx.commit()
                    messages.add_message(request, messages.SUCCESS, 'Accidente Desactivado exitosamente!')
                    return redirect("getAccidentesPage")
                else:
                    messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
                    return redirect("getAccidentesPage")
        except Exception as ex:
            print(ex)
            return redirect("getAccidentesPage")
    else:
        return redirect("getAccidentesPage")


def update_accidente(request):
    if (request.method == 'POST'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_accidente = request.POST.get("idAccidente")
                v_nombre_accidente = request.POST.get("txtNombreAccidente")
                v_descripcion_accidente = request.POST.get("txtDescripcionAccidente")
                v_fecha_accidente = request.POST.get("txtFechaAccidente")
                v_hora_accidente = request.POST.get("txtHoraAccidente")
                v_tipo_accidente = request.POST.get("txtTipoAccidente")
                v_status_accidente = 0

                cursor.execute("SELECT * FROM nma_accidentes WHERE id_accidente = %s" % (v_id_accidente))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("""UPDATE nma_accidentes SET nombre_accidente = '%s',
                    descripcion_accidente = '%s', fecha_accidente = %s, hora_accidente = %s, tipo_accidente = '%s', status_accidente = %s
                    WHERE id_accidente = %s """ % (v_nombre_accidente,v_descripcion_accidente, v_fecha_accidente, v_hora_accidente, v_tipo_accidente, v_status_accidente))

                    cx.commit()
                    return redirect("getAccidentesPage")
                
                else:
                    messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
                    return redirect("getAccidentesPage")

        except Exception as ex:
            # print(ex)
            messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
            return redirect("getAccidentesPage")
    else:
        return redirect("getAccidentesPage")

def get_accidentes (request):
    if(request.method=='GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_accidente = request.GET.get("idAccidente")
                v_nombre_accidente = request.GET.get("txtNombreAccidente")
                v_descripcion_accidente = request.GET.get("txtDescripcionAccidente")
                v_fecha_accidente = request.GET.get("txtFechaAccidente")
                v_hora_accidente = request.GET.get("txtHoraAccidente")
                v_tipo_accidente = request.GET.get("txtTipoAccidente")
                v_status_accidente = request.GET.get("txtStatusAccidente")

                cursor.execute("SELECT * FROM nma_accidentes WHERE id_accidente = %s" % (v_id_accidente))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("SELECT * FROM nma_accidentes")
                    # cursor.execute("""GET nma_accidentes GET nombre_accidente = '%s',
                    # descripcion_accidente = '%s', fecha_accidente = '%s', hora_accidente = '%s', tipo_accidente = '%s', status_accidente = '%s'
                    # WHERE id_accidente = '%s' """ % (v_nombre_accidente,v_descripcion_accidente, v_fecha_accidente, v_hora_accidente, v_tipo_accidente, v_status_accidente))

                    cx.commit()
                    return redirect("getAccidentesPage")
                
                else:
                    messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
                    return redirect("getAccidentesPage")

        except Exception as ex:
            # print(ex)
            messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
            return redirect("getAccidentesPage")
    else:
        return redirect("getAccidentesPage")

def delete_accidentes(request):
     if(request.method=='GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_accidente = request.GET.get("idAccidente")
                v_nombre_accidente = request.GET.get("txtNombreAccidente")
                v_descripcion_accidente = request.GET.get("txtDescripcionAccidente")
                v_fecha_accidente = request.GET.get("txtFechaAccidente")
                v_hora_accidente = request.GET.get("txtHoraAccidente")
                v_tipo_accidente = request.GET.get("txtTipoAccidente")
                v_status_accidente = request.GET.get("txtStatusAccidente")

                cursor.execute("SELECT * FROM nma_accidentes WHERE id_accidente = '%s'" % (v_id_accidente))
                exist = cursor.fetchall()
      

                if (exist != ()):
                    cursor.execute("""GET nma_accidentes DELETE nombre_accidente = '%s',
                    descripcion_accidente = '%s', fecha_accidente = '%s', hora_accidente = '%s', tipo_accidente = '%s', status_accidente = '%s'
                    WHERE id_accidente = '%s' """ % (v_nombre_accidente,v_descripcion_accidente, v_fecha_accidente, v_hora_accidente, v_tipo_accidente, v_status_accidente))

                    cx.commit()
                    return redirect("getAccidentesPage")
                
                else:
                    messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
                    return redirect("getAccidentesPage")

        except Exception as ex:
            # print(ex)
            messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
            return redirect("getAccidentesPage")
     else:
        return redirect("getAccidentesPage")

def getAllAccidentes(request):
    if(request.method == 'GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute("SELECT * FROM nma_accidentes")
                data_accidentes = cursor.fetchall()
                data_to_array = []
                for i in data_accidentes:
                    data_to_array.append({
                        "id_accidente" : i[0],
                        "nombre_accidente": i[1],
                        "descripcion_accidente": i[2],
                        "fecha_accidente": i[3],
                        "hora_accidente": i[4],
                        "tipo_accidente": i[5],
                        "status_accidente": i[6],
                    })

                for i in data_to_array:
                    if (i['status_accidente'] == 1):
                        i['status_accidente'] = """<div class='text-center'><button class='btn btn-sm btn-success' 
                            style='background: linear-gradient(to right, deepskyblue, blueviolet); border: none;'>Activado</button></div>"""
                    else:
                        i['status_accidente'] = """<div class='text-center'><button class='btn btn-sm btn-danger' 
                            style='background: linear-gradient(to right, orange, deeppink); border: none; color: white;'>Desactivado</button></div>"""

                    i['options'] = """
                        <div class='text-center'>
                            <button type='button' class='btn btn-sm btn-primary' onclick='fntEditAccidente(%s)' 
                                data-bs-toggle='modal' data-bs-target='#modalEditAccidente' style='background: linear-gradient(to right, deepskyblue, blueviolet);
                                border: none;'>
                                <i class='bx bxs-edit' ></i>                    
                            </button>
                            <a onclick='enableCliente(%s)' class='btn btn-sm btn-success'><i class='bx bx-power-off' ></i></a>
                            <a onclick='disableCliente(%s)' class='btn btn-sm btn-warning'><i class='bx bx-power-off' ></i></a>
                            <a onclick='deleteCliente(%s)' class='btn btn-sm btn-danger'><i class='bx bxs-trash-alt'></i></a>
                        </div>
                    """ % (i['id_accidente'],i['id_accidente'],i['id_accidente'],i['id_accidente'])

                return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as ex:
            print(ex)
            
    