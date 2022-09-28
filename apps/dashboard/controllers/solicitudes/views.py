from django.shortcuts import render, redirect
from django.http import JsonResponse
from .usp import *
from apps.dashboard.views import multiform
import apps.helpers as helpers

# Create your views here.

def dashboard_get_solicitudes_page(request):
    data = {
        'id' : 3,
        'meta_title': 'Dashboard - Solicitudes',
        'breadcrumb': "Solcitudes",
        'title': 'Lista de Solicitudes',
        'subtitle': 'Lista completa de solicitudes de Clientes',
    }

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
            i['status_solicitud'] = "<div class='text-center'><button class='btn btn-sm btn-success'><i class='bx bx-power-off'></i></button></div>"
        else:
            i['status_solicitud'] = "<div class='text-center'><button class='btn btn-sm btn-danger'><i class='bx bx-power-off'></i></button></div>"

        i['options'] = """
            <div class='text-center'>
                <button type='button' class='btn btn-sm btn-primary' onclick='fntEditSolicitud("%s")' data-bs-toggle='modal' data-bs-target='#modalEditSolicitud'><i class='bx bxs-edit' ></i></button>
                <a onclick='enableSolicitud(%s)' class='btn btn-sm btn-success'><i class='bx bx-power-off' ></i></a>
                <a onclick='disableSolicitud("%s")' class='btn btn-sm btn-warning'><i class='bx bx-power-off' ></i></a>
                <a onclick='deleteSolicitud("%s")' class='btn btn-sm btn-danger'><i class='bx bxs-trash-alt'></i></a>
            </div>
        """ % (i['id_solicitud'], i['id_solicitud'], i['id_solicitud'], i['id_solicitud'])

    for i in data_to_array:
        if (i['tipo_solicitud'] == 1):
            i['tipo_solicitud'] = "<div class='text-center'><button class='btn btn-sm btn-success'>Aseosría Especial</button></div>"
        elif (i['tipo_solicitud'] == 2):
            i['tipo_solicitud'] = "<div class='text-center'><button class='btn btn-sm btn-warning'>Capacitación</button></div>"
        elif (i['tipo_solicitud'] == 3):
            i['tipo_solicitud'] = "<div class='text-center'><button class='btn btn-sm btn-danger'>Accidente</button></div>"

    return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})

# GET UNA SOLICITUD
def getSolicitud(request):
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
                    "estado_solicitud": i[10],
                    "status_solicitud": i[11],
                })
            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return redirect("getSolicitudesPage")
    else:
        return redirect("getSolicitudesPage")

# UPDATE SOLICITUD
def updateSolicitud(request):
    if (request.method) == 'POST':
        v_id_solicitud = request.GET.get('idSolicitud')
        print (v_id_solicitud)
        exist = list(fc_get_solicitudes_dash(v_id_solicitud))
        # print (exist)
        if (exist != ()):
            v_fecha = request.POST.get("txtFecha")
            v_time_start = request.POST.get("txtTimeStart")
            v_time_end = request.POST.get("txtTimeEnd")

            fc_update_solicitud(v_id_solicitud, v_fecha, v_time_start, v_time_end)
            return redirect("getSolicitudesPage")
        else:
            return redirect("getSolicitudesPage")
    else:
        return redirect("getSolicitudesPage")
