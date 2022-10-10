from django.shortcuts import render, redirect
from django.http import JsonResponse
from .usp import *
from apps.dashboard.views import multiform
from django.contrib import messages
import apps.helpers as helpers
from apps.dashboard.views import get_connection
from django.contrib import messages

# Create your views here.

def dashboard_get_solicitudes_page(request):
    data = {
        'id' : 5,
        'meta_title': 'Dashboard - Solicitudes',
        'breadcrumb': "Solcitudes",
        'title': 'Lista de Solicitudes',
        'subtitle': 'Lista completa de solicitudes de Clientes',
    }

    a = helpers.session_user_exist(request)
    if (a == False):
        messages.add_message(request, messages.ERROR, 'No haz Iniciado Sesión.')
        return redirect ("loginDashboard")
    
    b = helpers.session_user_role(request)
    if (b == True):
        del request.session['usuario']
        messages.add_message(request, messages.ERROR, 'No tienes Permiso.')
        return redirect ("loginDashboard")
    
    c = helpers.request_module(request, data)
    if (c == True):
        return render(request, "solicitudes.html", data)

# LIST SOLICITUDES
def dashboard_get_all_solicitudes(request):
    data_solicitudes = list(fc_get_all_solicitudes())
    data_to_array = []
    # Convertir TUPLA a Array Modificable
    for i in data_solicitudes:
        data_to_array.append({
            "id_solicitud": i[0],
            "rut_cliente": i[1],
            "nombre_solicitud": i[4],
            "descripcion_solicitud": i[5],
            "tipo_solicitud": i[6],
            "status_solicitud": i[11],
            'fecha': i[7],
            'time_start': i[8],
            'time_end': i[9],
        })

    # Añadir HTML
    for i in data_to_array:
        if (i['status_solicitud'] == 1):
            i['status_solicitud'] = "<div class='text-center'><button class='btn btn-sm btn-success'>Activado</button></div>"
        else:
            i['status_solicitud'] = "<div class='text-center'><button class='btn btn-sm btn-danger'>Desactivado</button></div>"

        i['options'] = """
            <div class='text-center'>
                <button type='button' class='btn btn-sm btn-primary' onclick='fntEditSolicitud("%s")' data-bs-toggle='modal' data-bs-target='#modalEditSolicitud'><i class='bx bxs-edit' ></i></button>
                <a onclick='fntEnableSolicitud("%s")' class='btn btn-sm btn-success'><i class='bx bx-power-off' ></i></a>
                <a onclick='fntDisableSolicitud("%s")' class='btn btn-sm btn-warning'><i class='bx bx-power-off' ></i></a>
                <a onclick='fntConfirmDelete("%s")' class='btn btn-sm btn-danger'><i class='bx bxs-trash-alt'></i></a>
            </div>
        """ % (i['id_solicitud'], i['id_solicitud'], i['id_solicitud'], i['id_solicitud'])

    for i in data_to_array:
        if (i['tipo_solicitud'] == 1):
            i['tipo_solicitud'] = "<div class='text-center'><button class='btn btn-sm btn-success'>Asesoría Especial</button></div>"
        elif (i['tipo_solicitud'] == 2):
            i['tipo_solicitud'] = "<div class='text-center'><button class='btn btn-sm btn-warning'>Capacitación</button></div>"
        elif (i['tipo_solicitud'] == 3):
            i['tipo_solicitud'] = "<div class='text-center'><button class='btn btn-sm btn-danger'>Accidente</button></div>"

    return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})

# GET UNA SOLICITUD
def dashboard_get_solicitud(request):
    v_id_solicitud = request.GET.get('idSolicitud')
    if (v_id_solicitud != ""):
        data_solicitud = list(fc_get_solicitudes_dash(v_id_solicitud))
        data_to_array = []
        if (data_solicitud != ()):
            for i in data_solicitud:
                data_to_array.append({
                    "id_solicitud": i[0],
                    "fecha": i[7],
                    "time_start": i[8],
                    "time_end": i[9],
                    "status_solicitud": i[11],
                })
            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return redirect("getSolicitudesPage")
    else:
        return redirect("getSolicitudesPage")

# UPDATE SOLICITUD
def dashboard_update_solicitud(request):
    if (request.method) == 'POST':
        v_id_solicitud = request.POST.get("idSolicitud")
        exist = fc_get_solicitudes_dash(v_id_solicitud)
        # print (exist)
        if (exist != ()):
            v_fecha = request.POST.get("txtFecha")
            v_time_start = request.POST.get("txtTimeStart")
            v_time_end = request.POST.get("txtTimeEnd")

            fc_update_solicitud(v_id_solicitud, v_fecha, v_time_start, v_time_end)
            messages.add_message(request, messages.SUCCESS, 'Fecha y Hora solicitud actualizada')

            return redirect("getSolicitudesPage")
        else:
            messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado!')
            return redirect("getSolicitudesPage")
    else:
        messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado!')
        return redirect("getSolicitudesPage")

# ENABLE SOLICITUD
def dashboard_enable_solicitud(request):
    if (request.method) == 'GET':
        v_id_solicitud = request.GET.get("idSolicitud")
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute("SELECT * FROM nma_solicitudes WHERE id_solicitud = %s" % (v_id_solicitud))
                exist = fc_get_solicitudes_dash(v_id_solicitud)
                if (exist != ()):
                    cursor.execute("UPDATE nma_solicitudes SET status_solicitud = 1 WHERE id_solicitud = %s" % (v_id_solicitud))
                    cx.commit()
                    messages.add_message(request, messages.SUCCESS, 'Solicitud Activada!')
                    return redirect("getSolicitudesPage")
        except Exception as ex:
            print (ex)
            return redirect("getSolicitudesPage")
    else:
        return redirect("getSolicitudesPage")

# DISABLE SOLICITUD
def dashboard_disable_solicitud(request):
    if (request.method) == 'GET':
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_solicitud = request.GET.get("idSolicitud")
                cursor.execute("SELECT * from nma_solicitudes WHERE id_solicitud = %s" % (v_id_solicitud))
                exist = cursor.fetchall()
                print (exist)
                if (exist != ()):
                    cursor.execute("UPDATE nma_solicitudes SET status_solicitud = 0 WHERE id_solicitud = %s" % (v_id_solicitud))
                    cx.commit()
                    messages.add_message(request, messages.SUCCESS, 'Solicitud Desactivada!')
                    return redirect("getSolicitudesPage")
                else:
                    return redirect("getSolicitudesPage")
        except Exception as ex:
            print (ex)
            return redirect("getSolicitudesPage")
    else:
        return redirect("getSolicitudesPage")

# DELETE SOLICITUD
def dashboard_delete_solicitud(request):
    if (request.method) == 'GET':
        v_id_solicitud = request.GET.get("idSolicitud")
        exist = fc_get_solicitudes_dash(v_id_solicitud)
        if (exist != ()):
            fc_delete_solicitud(v_id_solicitud)
            messages.add_message(request, messages.SUCCESS, 'Solicitud Eliminada exitosamente!')
            return redirect("getSolicitudesPage")
        else:
            messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado!')
            return redirect("getSolicitudesPage")
    else:
        messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado!')
        return redirect("getSolicitudesPage")