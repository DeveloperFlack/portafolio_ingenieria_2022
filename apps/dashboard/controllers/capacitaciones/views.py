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
        'button_add': 'Añadir nueva capacitación',
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
            v_rut =  request.session['profesional']['rut_usuario']
            v_nombre_capacitacion = request.POST.get("txtNombreCapacitacion")
            v_descripcion_capacitacion = request.POST.get("txtDescripcionCapacitacion")
            v_total_capacitacion = request.POST.get("txtTotalCapacitacion")

            fc_insert_capacitacion(v_rut, v_nombre_capacitacion, v_descripcion_capacitacion, v_total_capacitacion)

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
            "status_capacitaciones": i[5],
        })
    
    # Añadir HTML}
    for i in data_to_array:
        if (i['status_capacitaciones'] == 1):
            i['status_capacitaciones'] = """<div class='text-center'><button class='btn btn-sm btn-success' 
                style='background: linear-gradient(to right, deepskyblue, blueviolet); border: none;'>Activado</button></div>"""
        else:
            i['status_capacitaciones'] = """<div class='text-center'><button class='btn btn-sm btn-danger' 
                style='background: linear-gradient(to right, orange, deeppink); border: none; color: white;'>Desactivado</button></div>"""

    # Añadir HTML
    for i in range(len(data_to_array)):
        data_to_array[i]['actividades'] = """
            <div class='text-center'>
                <button type='button' class='btn btn-sm btn-success' onclick='fntEditActividadesCapacitacion(%s)'  
                    data-bs-toggle='modal' data-bs-target='#modalActividades'>
                    <i class='bx bx-plus' ></i>
                </button>            
            </div>
        """ % (data_to_array[i]['id_capacitacion'])
    # Añadir HTML
    for i in data_to_array:
        i['options'] = """
            <div class='text-center'>
                <button type='button' class='btn btn-sm btn-primary' onclick='fntEditCapacitacion(%s)' 
                    data-bs-toggle='modal' data-bs-target='#modalCapacitaciones' style='background: linear-gradient(to right, deepskyblue, blueviolet);
                    border: none;'>
                    <i class='bx bxs-edit' ></i>
                </button>
                <a onclick='fntEnableCapacitacion(%s)' class='btn btn-sm btn-success'><i class='bx bx-power-off' ></i></a>
                <a onclick='fntDisableCapacitacion(%s)' class='btn btn-sm btn-warning'><i class='bx bx-power-off' ></i></a>
                <a onclick='fntConfirmDelete(%s)' class='btn btn-sm btn-danger'><i class='bx bxs-trash-alt'></i></a>
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
                    "status_capacitaciones": i[5],
                })
            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return redirect("getCapacitacionesPage")
    else:
        return redirect("getCapacitacionesPage")

# DELETE CAPACITACIÓN
def dashboard_delete_capacitacion(request):
    if (request.method) == 'GET':
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_capacitacion = request.GET.get("idCapacitacion")
                cursor.execute("SELECT * FROM nma_capacitacion WHERE id_capacitacion = %s" % (v_id_capacitacion))
                exist = cursor.fetchall()
                
                if (exist != ()):
                    cursor.execute("DELETE FROM nma_capacitacion WHERE id_capacitacion = %s" % (v_id_capacitacion))
                    cx.commit()
            cx.close()
            return redirect ('getCapacitacionesPage')
        except Exception as ex:
            print (ex)
            return redirect ('getCapacitacionesPage')
    else:
        messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado!')
        return redirect("getCapacitacionesPage")

def dashoard_disable_capacitacion(request):
    if (request.method == 'GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_capacitacion = request.GET.get('idCapacitacion')
                cursor.execute("SELECT * FROM nma_capacitacion WHERE id_capacitacion = %s" % (v_id_capacitacion))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("UPDATE nma_capacitacion SET status_capacitaciones = 0 WHERE id_capacitacion = %s" % (v_id_capacitacion))
                    cx.commit()
                    return redirect("getAsesoriasPage")
                else:
                    messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
                    return redirect("getAsesoriasPage")
        except Exception as ex:
            print(ex)
            return redirect("getAsesoriasPage")
    else:
        return redirect("getAsesoriasPage")

def dashoard_enable_capacitacion(request):
    if (request.method == 'GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_capacitacion = request.GET.get('idCapacitacion')
                cursor.execute("SELECT * FROM nma_capacitacion WHERE id_capacitacion = %s" % (v_id_capacitacion))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("UPDATE nma_capacitacion SET status_capacitaciones = 1 WHERE id_capacitacion = %s" % (v_id_capacitacion))
                    cx.commit()
                    return redirect("getAsesoriasPage")
                else:
                    messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
                    return redirect("getAsesoriasPage")
        except Exception as ex:
            print(ex)
            return redirect("getAsesoriasPage")
    else:
        return redirect("getAsesoriasPage")

def dashboard_insert_actividades(request):
    x = 'usuario' in request.session
    if (x == False):
        return redirect ("loginDashboard")

    if (request.method == "POST"):
        v_idCapacitacion = request.GET.get('idCapacitacion')
        print(v_idCapacitacion)
        
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                if (v_idCapacitacion == ""):
                    print("entro en el with if")
                    # Obtener los datos del formulario e insertarlos en la base de datos.
                    v_nombre_actividad1= request.POST.get("txtNombreActividad1")
                    v_nombre_actividad2= request.POST.get("txtNombreActividad2")
                    v_nombre_actividad3= request.POST.get("txtNombreActividad3")
                    v_nombre_actividad4= request.POST.get("txtNombreActividad4")
                    v_nombre_actividad5= request.POST.get("txtNombreActividad5")
                    v_descripcion_actividad = request.POST.get("txtDescripcionActividades")

                    cursor.execute("""INSERT INTO nma_actividad (nombre_actividad_1, nombre_actividad_2, nombre_actividad_3, nombre_actividad_4, nombre_actividad_5, descripcion_actividad, id_capacitacion) 
                                    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %s)""" % (v_nombre_actividad1, v_nombre_actividad2, v_nombre_actividad3, v_nombre_actividad4, v_nombre_actividad5, v_descripcion_actividad, v_idCapacitacion))
                    cx.commit()    
                else:
                    # ACTUALIZAR Actividad                   
                    if (v_idCapacitacion != ""):                    
                        # Obtener los datos del formulario e actualizarlos en la base de datos.
                        v_nombre_actividad1= request.POST.get("txtNombreActividad1")
                        v_nombre_actividad2= request.POST.get("txtNombreActividad2")
                        v_nombre_actividad3= request.POST.get("txtNombreActividad3")
                        v_nombre_actividad4= request.POST.get("txtNombreActividad4")
                        v_nombre_actividad5= request.POST.get("txtNombreActividad5")
                        v_descripcion_actividad = request.POST.get("txtDescripcionActividades")

                        cursor.execute(""" update nma_actividad set nombre_actividad_1 = '%s', nombre_actividad_2 = '%s', nombre_actividad_3 = '%s', nombre_actividad_4 = '%s', nombre_actividad_5 = '%s', descripcion_actividad = '%s' where id_capacitacion = %s""" % (v_nombre_actividad1, v_nombre_actividad2, v_nombre_actividad3, v_nombre_actividad4, v_nombre_actividad5, v_descripcion_actividad, v_idCapacitacion))
                        cx.commit()  

                        return redirect("getCapacitacionesPage")
                    else:
                        messages.add_message(request, messages.ERROR, 'Ha ocurrido un error, vuelva a intentarlo!')
                        return redirect("getCapacitacionesPage")            
            cx.close()
            return redirect ('getCapacitacionesPage')
        except Exception as ex:
            print (ex)
            return redirect ('getCapacitacionesPage')
    else:
        return redirect ('getCapacitacionesPage')

def getActividad(request):
    v_idCapacitacion = request.GET.get('idCapacitacion')
    if (v_idCapacitacion != ""):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute(""" SELECT * FROM nma_actividad WHERE id_capacitacion = %s """ % (v_idCapacitacion))
                data_to_array = []
                if (cursor != ()):
                    for i in cursor:
                        data_to_array.append({
                            "id_capacitacion": i[7],
                            "nombre_actividad_1": i[1],
                            "nombre_actividad_2": i[2],
                            "nombre_actividad_3": i[3],
                            "nombre_actividad_4": i[4],
                            "nombre_actividad_5": i[5],
                            "descripcion_actividad": i[6],
                        })
                    
                    return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
                else:
                    return redirect("getCapacitacionesPage")
        except Exception as ex:
            print (ex)
            return redirect ('getCapacitacionesPage')            
    else:
        return redirect("getCapacitacionesPage")