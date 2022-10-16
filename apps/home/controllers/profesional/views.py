from genericpath import exists
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
        'session_status' : request_session(request),
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
        'session_status' : request_session(request)
    }
    return render(request, 'modules/reporte_global.html', data)



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