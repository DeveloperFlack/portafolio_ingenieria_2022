from django.shortcuts import render, redirect
from django.http import JsonResponse
from .usp import *
import apps.helpers as helpers
from django.contrib import messages

def getCapacitacionesPage(request):
    data = {
        'id' : 7,
        'meta_title': 'Dashboard - Capacitaciones',
        'breadcrumb': "Capacitaciones",
        'title': 'Lista de Capacitaciones',
        'subtitle': 'Lista completa de capacitaciones',
        'button_add': 'Añadir Capacitación',
    }
    return render(request, "capacitaciones.html", data)

# INSERTAR UNA CAPACITACIÓN
def insertCapacitacion(request):
    x = 'usuario' in request.session
    
    if (x == False):
        return redirect ("loginDashboard")

    if request.method == "POST":
        v_idCapacitacion = request.POST.get("idCapacitacion")
        if (v_idCapacitacion == ""):
            # INSERTAR CAPACITACIÓN
            # Obtener los datos del formulario e insertarlos en la base de datos.
            v_nombre_capacitacion = request.POST.get("txtNombreCapacitacion")
            v_descripcion_capacitacion = request.POST.get("txtDescripcionCapacitacion")
            v_total_capacitacion = request.POST.get("txtTotalCapacitacion")

            messages.add_message(request, messages.SUCCESS, 'Capacitación creada exitosamente!')
            fc_insert_capacitacion(v_nombre_capacitacion, v_descripcion_capacitacion, v_total_capacitacion)

            return redirect("getCapacitacionesPage")

        else:
            # ACTUALIZAR CAPACITACIÓN
            # Verificando si la capacitación existe, si existe, actualiza la capacitación, si no, redirige a
            # getCapacitacionesPage.
            exist = fc_get_capacitacion(v_idCapacitacion)
            if (exist != ()):
                v_nombre_capacitacion = request.POST.get("txtNombreCapacitacion")
                v_descripcion_capacitacion = request.POST.get("txtDescripcionCapacitacion")
                v_total_capacitacion = request.POST.get("txtTotalCapacitacion")

                fc_update_capacitacion(v_idCapacitacion, v_nombre_capacitacion, v_descripcion_capacitacion, v_total_capacitacion)
                messages.add_message(request, messages.SUCCESS, 'Capacitación actualizada!')

                return redirect("getCapacitacionesPage")
            else:
                messages.add_message(request, messages.ERROR, 'Ha ocurrido un error, vuelva a intentarlo!')
                return redirect("getCapacitacionesPage")
    else:
        messages.add_message(request, messages.ERROR, 'Ha ocurrido un error, vuelva a intentarlo!')
        return redirect("getCapacitacionesPage")

# OBTENER TODAS LAS CAPACITACIONES
def getAllCapacitaciones(request):
    data_capacitaciones = list(fc_get_all_capacitaciones())
    data_to_array = []
    # Convertir TUPLA a Array Modificable
    for i in data_capacitaciones:
        data_to_array.append({
            "id_capacitacion": i[0],
            "nombre_capacitacion": i[2],
            "descripcion_capacitacion": i[3],
            "total_capacitacion": i[4],
        })

    # Añadir HTML
    for i in data_to_array:
        i['usuarios'] = """
            <div class='text-center'>
                <button class="btn btn-sm btn-primary form-control" name="txtRutUsuario" id="txtRutUsuario" style="width: fit-content;"><i class='bx bxs-edit' ></i></button>
            </div>
        """
    # Añadir HTML
    for i in data_to_array:
        i['options'] = """
            <div class='text-center'>
                <button type='button' class='btn btn-sm btn-primary' onclick='fntEditCapacitacion(%s)' data-bs-toggle='modal' data-bs-target='#modalCapacitaciones'><i class='bx bxs-edit' ></i></button>
                <a onclick='enableModule(%s)' class='btn btn-sm btn-success'><i class='bx bx-power-off' ></i></a>
                <a onclick='disableModule(%s)' class='btn btn-sm btn-warning'><i class='bx bx-power-off' ></i></a>
                <a onclick='fntDeleteCapacitacion(%s)' class='btn btn-sm btn-danger'><i class='bx bxs-trash-alt'></i></a>
            </div>
        """ % (i['id_capacitacion'], i['id_capacitacion'], i['id_capacitacion'], i['id_capacitacion'])

    return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})

# OBTENER UNA CAPACITACIÓN
def getCapacitacion(request):
    v_idCapacitacion = request.GET.get('idCapacitacion')
    if (v_idCapacitacion != ""):
        data_capacitaciones = list(fc_get_capacitacion(v_idCapacitacion))
        data_to_array = []
        if (data_capacitaciones != ()):
            for i in data_capacitaciones:
                data_to_array.append({
                    "id_capacitacion": i[0],
                    "nombre_capacitacion": i[2],
                    "descripcion_capacitacion": i[3],
                    "total_capacitacion": i[4],
                })
            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return redirect("getCapacitacionesPage")
    else:
        return redirect("getCapacitacionesPage")

# DELETE CAPACITACIÓN
def dashboard_delete_capacitacion(request):
    if (request.method) == 'GET':
        v_id_capacitacion = request.GET.get("idCapacitacion")
        exist = fc_get_capacitacion(v_id_capacitacion)
        if (exist != ()):
            fc_delete_capacitacion(v_id_capacitacion)
            messages.add_message(request, messages.SUCCESS, 'Capacitación Eliminada exitosamente!')
            return redirect("getCapacitacionesPage")
        else:
            messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado!')
            return redirect("getCapacitacionesPage")
    else:
        messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado!')
        return redirect("getCapacitacionesPage")