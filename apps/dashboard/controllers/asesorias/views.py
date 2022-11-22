from genericpath import exists
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .usp import *
import apps.helpers as helpers
from django.contrib import messages

def getAsesoriasPage(request):
    data = {
        'id' : 10,
        'meta_title': 'Dashboard - Asesorías',
        'breadcrumb': "Asesorías",
        'title': 'Lista de Asesorías',
        'subtitle': 'Lista completa de Asesorías',
        'button_add': 'Añadir nueva asesoría',
    }
    return render(request, "asesorias.html", data)

# Insertar una Aseosria
def insertAsesoria(request):
    x = 'usuario' in request.session

    if (x == False):
        return redirect (loginDashboard)
    
    if request.method == "POST":
        v_idAsesoria = request.POST.get("idAsesoria")
        if (v_idAsesoria == ""):
            #Insertar asesoria
            #Obtener los datos del formulario e insertarlos en la base de datos.
            v_nombre_asesoria = request.POST.get("txtNombreAsesoria")
            v_descripcion_asesoria = request.POST.get("txtDescripcionAsesoria")
            v_total_asesoria = request.POST.get("txtTotalAsesoria")
            v_rut_user_session = request.session['usuario']['RUT']

            fc_insert_asesorias(v_rut_user_session, v_nombre_asesoria, v_descripcion_asesoria, v_total_asesoria)
            # messages.add_message(request, messages.SUCCESS, 'Asesoría creada exitosamente!')

            return redirect("getAsesoriasPage")
        
        else:
            #Actualizar Asesoria
            #Verificando si la asesoria existe, si existe, actualiza la asesoria, si no, redirige a 
            #getAsesoriasPage
            exist = fc_get_asesoria(v_idAsesoria)
            if (exist != ()):
                v_nombre_asesoria = request.POST.get("txtNombreAsesoria")
                v_descripcion_asesoria = request.POST.get("txtDescripcionAsesoria")
                v_total_asesoria = request.POST.get("txtTotalAsesoria")
                v_rut_usuario_session = request.session['usuario']['RUT']

                fc_update_asesoria(v_idAsesoria, v_rut_usuario_session, v_nombre_asesoria, v_descripcion_asesoria, v_total_asesoria)

                return redirect("getAsesoriasPage")
            else:
                messages.add_message(request, messages.ERROR, 'Ha ocurrido un error, vuelva a intentarlo!')
                return redirect("getAsesoriasPage")
    else:
        messages.add_message(request, messages.ERROR, 'Ha ocurrido un error, vuelva a intentarlo!')
        return redirect("getAsesoriasPage")

#Obtener Todas las Asesorias
def getALLAsesorias(request):
    data_asesoria = list(fc_get_all_asesorias())
    data_to_array = []
    #Convertir TUPLA a Array Modificable
    for i in data_asesoria:
        data_to_array.append({
            "id_asesoria": i[0],
            "nombre_asesoria": i[2],
            "descripcion_asesoria": i[3],
            "total_asesoria": i[4],
            "status_asesoria": i[5],
        })
    
    # Añadir HTML}
    for i in data_to_array:
        if (i['status_asesoria'] == 1):
            i['status_asesoria'] = """<div class='text-center'><button class='btn btn-sm btn-success' 
                style='background: linear-gradient(to right, deepskyblue, blueviolet); border: none;'>Activado</button></div>"""
        else:
            i['status_asesoria'] = """<div class='text-center'><button class='btn btn-sm btn-danger' 
                style='background: linear-gradient(to right, orange, deeppink); border: none; color: white;'>Desactivado</button></div>"""

    # Añadir HTML
    for i in data_to_array:
        i['options'] = """
            <div class='text-center'>
                <button type='button' class='btn btn-sm btn-primary' onclick='fntEditAsesoria(%s)' 
                    data-bs-toggle='modal' data-bs-target='#modalAsesoria' style='background: linear-gradient(to right, deepskyblue, blueviolet);
                    border: none;'>
                    <i class='bx bxs-edit' ></i>
                </button>
                <a onclick='fntEnableAsesoria(%s)' class='btn btn-sm btn-success'><i class='bx bx-power-off' ></i></a>
                <a onclick='fntDisableAsesoria(%s)' class='btn btn-sm btn-warning'><i class='bx bx-power-off' ></i></a>
                <a onclick='fntConfirmDelete(%s)' class='btn btn-sm btn-danger'><i class='bx bxs-trash-alt'></i></a>
            </div>
        """ % (i['id_asesoria'], i['id_asesoria'], i['id_asesoria'], i['id_asesoria'])

    return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})

#Obtener una Asesoria
def getAsesoria(request):
    v_idAsesoria = request.GET.get('idAsesoria')
    if (v_idAsesoria != ""):
        data_asesoria = list(fc_get_asesoria(v_idAsesoria))
        data_to_array = []
        if (data_asesoria != ()):
            for i in data_asesoria:
                data_to_array.append({
                    "id_asesoria": i[0],
                    "nombre_asesoria": i[2],
                    "descripcion_asesoria": i[3],
                    "total_asesoria": i[4],
                    "status_asesoria": i[5],
                })
            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return redirect("getAsesoriasPage")
    else:
        return redirect("getAsesoriasPage")

#Delete Asesoria
def dashboard_delete_asesoria(request):
    if (request.method) == 'GET':
        v_id_asesoria = request.GET.get("idAsesoria")
        exist = fc_get_asesoria(v_id_asesoria)
        if (exist != ()):
            fc_delete_asesoria(v_id_asesoria)
            messages.add_message(request, messages.SUCCESS, 'Asesoria Eliminada exitosamente!')
            return redirect("getAsesoriasPage")
        else:
            messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado!')
            return redirect("getAsesoriasPage")
    else:
        messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado!')
        return redirect("getAsesoriasPage")

def dashoard_disable_asesoria(request):
    if (request.method == 'GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_asesoria = request.GET.get('idAsesoria')
                cursor.execute("SELECT * FROM nma_asesoria WHERE id_asesoria = '%s'" % (v_id_asesoria))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("UPDATE nma_asesoria SET status_asesoria = 0 WHERE id_asesoria = '%s'" % (v_id_asesoria))
                    cx.commit()
                    messages.add_message(request, messages.SUCCESS, 'Asesoria Desactivada exitosamente!')
                    return redirect("getAsesoriasPage")
                else:
                    messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
                    return redirect("getAsesoriasPage")
        except Exception as ex:
            print(ex)
            return redirect("getAsesoriasPage")
    else:
        return redirect("getAsesoriasPage")

def dashboard_enable_asesoria(request):
    if (request.method == 'GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_asesoria = request.GET.get('idAsesoria')
                cursor.execute("SELECT * FROM nma_asesoria WHERE id_asesoria = '%s'" % (v_id_asesoria))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("UPDATE nma_asesoria SET status_asesoria = 1 WHERE id_asesoria = '%s'" % (v_id_asesoria))
                    cx.commit()
                    messages.add_message(request, messages.SUCCESS, 'Asesoria Activada exitosamente!')
                    return redirect("getAsesoriasPage")
                else:
                    messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
                    return redirect("getAsesoriasPage")
        except Exception as ex:
            print(ex)
            return redirect("getAsesoriasPage")
    else:
        return redirect("getAsesoriasPage")
