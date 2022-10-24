from datetime import date , datetime
from genericpath import exists
from zoneinfo import ZoneInfo
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .usp import *
from apps.home.views import get_connection
from apps.dashboard.controllers.usuarios.usp import *
from django.contrib import messages
from apps.helpers import request_session_profesional, request_session

def portal_profesional(request):
    status = request_session_profesional(request)
    if (status == False):
        return redirect('getHome')
   
    data = {
        'session_status' : request_session(request)

    }
    return render(request, 'portal-professional.html', data)

def projects_profesional(request): 
    status = request_session_profesional(request)
    if (status == False):
        return redirect('getHome')
    
    data = {
        'session_status' : request_session(request),
        'capacitaciones' : get_all_project_professional(request)
    }
    return render(request, 'modules/projects-professional.html', data)

def tickets_profesional(request): 
    status = request_session_profesional(request)
    if (status == False):
        return redirect('getHome')
    
    data = {
        'session_status' : request_session(request)
    }
    return render(request, 'modules/tickets-professional.html', data)

def reportes_globales_profesional(request): 
    status = request_session_profesional(request)
    if (status == False):
        return redirect('getHome')
    
    data = {
        'session_status' : request_session(request),
        'proyectos' : get_capacitaciones(request),
        'clientes' : get_all_clientes(request)
    }
    return render(request, 'modules/reporte_global.html', data)

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

def insert_project (request):
    if (request.method == 'POST'):
        v_id = request.POST.get('numberCapacitacion')
        v_rut =  request.session['profesional']['rut_usuario']
        if (v_id == ""):
            v_id = 0
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute("SELECT * FROM nma_capacitacion WHERE (id_capacitacion = %s and rut_usuario = '%s' )" % (v_id, v_rut))
                exist = cursor.fetchall()
                
                if (exist == ()):
                    v_nombreCapacitacion = request.POST.get('txtNombreCapacitacionProfesional')
                    v_descripcionCapacitacion = request.POST.get('txtDescripcionCapacitacionProfessional')
                    v_totalCapacitacion = request.POST.get('intTotalCapacitacion')
                    v_listStatus = request.POST.get('listStatusCapacitacion')
                    cursor.execute("""INSERT INTO nma_capacitacion (rut_usuario, nombre_capacitacion, descripcion_capacitacion, total_capacitacion, status_capacitaciones ) 
                                    VALUES ('%s', '%s', '%s', %s, %s)""" % (v_rut, v_nombreCapacitacion, v_descripcionCapacitacion, v_totalCapacitacion, v_listStatus))
                    cx.commit()
                else:
                    v_nombreCapacitacion = request.POST.get('txtNombreCapacitacionProfesional')
                    v_descripcionCapacitacion = request.POST.get('txtDescripcionCapacitacionProfessional')
                    v_totalCapacitacion = request.POST.get('intTotalCapacitacion')
                    v_listStatus = request.POST.get('listStatusCapacitacion')
                    cursor.execute("""UPDATE nma_capacitacion SET nombre_capacitacion = '%s',  descripcion_capacitacion = '%s',  total_capacitacion = %s,  status_capacitaciones = %s
                                    WHERE (id_capacitacion = %s AND rut_usuario = '%s') """ % 
                                    (v_nombreCapacitacion, v_descripcionCapacitacion, v_totalCapacitacion, v_listStatus, v_id, v_rut))
                    cx.commit()
            cx.close()
            return redirect ('projectsProfesional')
        except Exception as ex:
            print (ex)
            return redirect ('projectsProfesional')
    else:
        return redirect ('projectsProfesional')

def get_all_project_professional (request):
    v_rut = request.session['profesional']['rut_usuario']
    try:
        cx = get_connection()
        
        with cx.cursor() as cursor:
            cursor.execute("SELECT * FROM nma_capacitacion WHERE rut_usuario = '%s' " % (v_rut))
            datos = cursor.fetchall()
            # print (datos)
            data_to_array = []
            
            for i in datos:
                data_to_array.append({
                    'id_capacitacion' : i[0],
                    'rut_usuario' : i[1],
                    'nombre_capacitacion' : i[2],
                    'descripcion_capacitacion' : i[3],
                    'total_capacitacion' : i[4],
                    'status_capacitacion' : i[5],
                })
            for x in range(len(data_to_array)):
                data_to_array[x]['options'] = """
                    <div class="text-center">
                        <button type='button' class='btn btn-sm btn-primary' onclick='fntEditProject(%s)'
                            data-bs-toggle='modal' data-bs-target='#modalProject' style='background: linear-gradient(to right, deepskyblue, blueviolet);
                            border: none; border-radius: 3px !important;'>
                            <i class='bx bxs-edit' ></i>
                        </button>
                        <button onclick="fntConfirmDelete(%s)" class="btn btn-sm btn-danger" style='border-radius: 3px !important;'><i class='bx bx-trash'></i></button>
                    </div>
                """ % (data_to_array[x]['id_capacitacion'], data_to_array[x]['id_capacitacion'])
            # print (data_to_array)
            return (data_to_array)
    except Exception as ex:
        print (ex)
        return redirect ('projectsProfesional')

def delete_capacitacion (request):
    if (request.method  == 'GET'):
        v_id = request.GET.get('numberCapacitacion')
        v_rut =  request.session['profesional']['rut_usuario']
        if (v_id == ""):
            v_id = 0
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute("SELECT * FROM nma_capacitacion WHERE (id_capacitacion = %s and rut_usuario = '%s' )" % (v_id, v_rut))
                exist = cursor.fetchall()
                
                if (exist != ()):
                    cursor.execute("DELETE FROM nma_capacitacion WHERE (id_capacitacion = %s and rut_usuario = '%s' )" % (v_id, v_rut))
                    cx.commit()
            cx.close()
            return redirect ('projectsProfesional')
        except Exception as ex:
            print (ex)
            return redirect ('projectsProfesional')
    else:
        return redirect ('projectsProfesional')
    
def get_capacitacion(request):
    if (request.method  == 'GET'):
        v_id = request.GET.get('numberCapacitacion')
        v_rut =  request.session['profesional']['rut_usuario']
        if (v_id == ""):
            v_id = 0
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute("SELECT * FROM nma_capacitacion WHERE (id_capacitacion = %s and rut_usuario = '%s' )" % (v_id, v_rut))
                exist = cursor.fetchall()
                data_to_array = []
                """ nombre_capacitacion = '%s', 
                                        descripcion_capacitacion = '%s', 
                                        total_capacitacion = '%s', 
                                        status_capacitaciones = '%s')  """
                if (exist != ()):
                    for i in exist:
                        data_to_array.append({
                            "id_capacitacion": i[0],
                            "rut_usuario": i[1],
                            "nombre_capacitacion" : i[2],
                            "descripcion_capacitacion": i[3],
                            "total_capacitacion": i[4],
                            "status_capacitacion": i[5],
                    })
            cx.close()
            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as ex:
            print (ex)
            return redirect ('projectsProfesional')
    else:
        return redirect ('projectsProfesional')

def insert_reporteglobal (request):
    if (request.method == 'POST'):
        v_id = request.POST.get('folioReporte')
        v_rut_profesional =  request.session['profesional']['rut_usuario']
        # v_rut_cliente = 0
        if (v_id == ""):
            v_id = 0
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute("""SELECT * FROM nma_reportes where id= '%s' """ % (v_id))
                exist = cursor.fetchall()
                if (exist == ()):
                    v_nombreReporte = request.POST.get('txtNombreReporte')
                    v_descripcionReporte = request.POST.get('txtDescripcionReporte')                    
                    v_fecha_utc = date.today()
                    v_rut_usuario = v_rut_profesional
                    v_rut_cliente = request.POST.get('listrutCliente')
                    v_idProyecto= request.POST.get('listProjects')
                    # print(v_rut_cliente)
                    cursor.execute("""INSERT INTO nma_reportes (nombre, descripcion, create_time, rut_usuario, rut_cliente, id_proyecto ) 
                                    VALUES ('%s', '%s', '%s', '%s', '%s', %s)""" % (v_nombreReporte, v_descripcionReporte, v_fecha_utc, v_rut_usuario, v_rut_cliente, v_idProyecto))
                    cx.commit()

                else:
                    v_nombreReporte = request.POST.get('txtNombreReporte')
                    v_descripcionReporte = request.POST.get('txtDescripcionReporte')                    
                    v_fecha_utc = date.today()
                    v_rut_usuario = request.session['profesional']['rut_usuario']
                    v_rut_cliente = request.POST.get('listrutCliente')
                    v_idProyecto= request.POST.get('listProjects') 
                    # print(v_rut_cliente)
                    print("update")
                    cursor.execute("""UPDATE nma_reportes SET nombre = '%s',  descripcion = '%s',  create_time = '%s',  rut_usuario = '%s' , rut_cliente = '%s' , id_proyecto = %s
                                WHERE (id = %s AND rut_usuario = '%s') """ % 
                                (v_nombreReporte, v_descripcionReporte, v_fecha_utc, v_rut_usuario, v_rut_cliente, v_idProyecto, v_id, v_rut_usuario))
                    cx.commit()
            cx.close()
            return redirect ('reportesGlobalesProfesional')
        except Exception as ex:
            print (ex)
            return redirect ('reportesGlobalesProfesional')
    else:
        return redirect ('reportesGlobalesProfesional')

def get_all_reportes_globales (request):
    v_rut = request.session['profesional']['rut_usuario']
    try:
        cx = get_connection()
        
        with cx.cursor() as cursor:
            cursor.execute("SELECT * FROM nma_reportes WHERE rut_usuario = '%s' " % (v_rut))
            datos = cursor.fetchall()
            
            data_to_array = []
            
            for i in datos:
                data_to_array.append({
                    'id' : i[0],
                    'nombre' : i[1],
                    'descripcion' : i[2],
                    'create_time' : i[3],
                    'rut_usuario' : i[4],
                    'rut_cliente' : i[5],
                    'id_proyecto' : i[6],
                })
            for x in range(len(data_to_array)):
                data_to_array[x]['options'] = """
                    <div class="text-center">
                        <button type='button' class='btn btn-sm btn-primary' onclick='fntEditReporte(%s)'
                            data-bs-toggle='modal' data-bs-target='#modalReporte' style='background: linear-gradient(to right, deepskyblue, blueviolet);
                            border: none; border-radius: 3px !important;'>
                            <i class='bx bxs-edit' ></i>
                        </button>
                        <button onclick="fntConfirmDelete(%s)" class="btn btn-sm btn-danger" style='border-radius: 3px !important;'><i class='bx bx-trash'></i></button>
                    </div>
                """ % (data_to_array[x]['id'], data_to_array[x]['id'])
            # print (data_to_array)
            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
    except Exception as ex:
        print (ex)
        return redirect ('reportesGlobalesProfesional')

def get_reportesGlobal (request):
    if (request.method == 'GET'):
        v_id =  request.GET.get('idReporte')
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute("""SELECT * FROM nma_reportes WHERE id = '%s' """ % (v_id))
                data_reportes = cursor.fetchall()
                data_to_array = []
                
                for i in range(len(data_reportes)):
                    data_to_array.append({
                        "id" : data_reportes[i][0],
                        "nombre" : data_reportes[i][1],
                        "descripcion" : data_reportes[i][2],
                        "create_time" : data_reportes[i][3],
                        "rut_usuario" : data_reportes[i][4],
                        "rut_cliente" : data_reportes[i][5],
                        "id_proyecto" : data_reportes[i][6],
                    })
                
                return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as ex:
            print (ex)
    else:
        return redirect ('reportesGlobalesProfesional')

# DELETE CAPACITACIÓN
def delete_reporte(request):
    if (request.method) == 'GET':
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_reporte = request.GET.get("idReporte")
                cursor.execute("""SELECT * FROM nma_reportes WHERE id = %s""" % (v_id_reporte))
                exist = cursor.fetchall()
                
                if (exist != ()):
                    cursor.execute("""DELETE FROM nma_reportes WHERE id = %s""" % (v_id_reporte))
                    cx.commit()
            cx.close()
            return redirect ('reportesGlobalesProfesional')
        except Exception as ex:
            print (ex)
            return redirect ('reportesGlobalesProfesional')
    else:
        messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado!')
        return redirect("reportesGlobalesProfesional")

def get_all_clientes(request):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("""SELECT rut_cliente,n1_cliente,ap_cliente FROM nma_cliente """)
            data_clientes = cursor.fetchall()
            data_to_array = []
            
            for i in range(len(data_clientes)):
                data_to_array.append({
                    "rut_cliente" : data_clientes[i][0],
                    "n1_cliente" : data_clientes[i][1],
                    "ap_cliente" : data_clientes[i][2],
                })
            # print(data_to_array)
            return (data_to_array)
    except Exception as ex:
        print (ex)

