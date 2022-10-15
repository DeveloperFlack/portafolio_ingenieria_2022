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
def insertAccidentes(request):
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

def disable_accidente(request):
    if (request.method == 'GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_accidente = request.GET.get('idAccidente')
                cursor.execute("SELECT * FROM nma_accidente WHERE id_accidente = '%s'" % (v_id_accidente))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("UPDATE nma_accidentes SET status_accidente = 0 WHERE id_accidente = '%s'" % (v_id_accidente))
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
                cursor.execute("SELECT * FROM nma_accidente WHERE id_accidente = '%s'" % (v_id_accidente))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("UPDATE nma_accidentes SET status_accidente = 1 WHERE id_accidente = '%s'" % (v_id_accidente))
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
                v_status_accidente = request.POST.get("txtStatusAccidente")

                cursor.execute("SELECT * FROM nma_accidentes WHERE id_accidente = '%s'" % (v_id_accidente))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("""UPDATE nma_accidentes SET nombre_accidente = '%s',
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

                cursor.execute("SELECT * FROM nma_accidentes WHERE id_accidente = '%s'" % (v_id_accidente))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("""GET nma_accidentes GET nombre_accidente = '%s',
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