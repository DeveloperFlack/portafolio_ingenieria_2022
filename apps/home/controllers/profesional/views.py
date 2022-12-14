from datetime import date, datetime
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
        'session_status': request_session(request),
    }

    return render(request, 'portal-professional.html', data)


def projects_profesional(request):
    status = request_session_profesional(request)
    if (status == False):
        return redirect('getHome')

    data = {
        'session_status': request_session(request),
        'capacitaciones': get_all_project_professional(request),
    }

    return render(request, 'modules/projects-professional.html', data)


def tickets_profesional(request):
    status = request_session_profesional(request)
    if (status == False):
        return redirect('getHome')

    data = {
        'session_status': request_session(request)
    }

    return render(request, 'modules/tickets-professional.html', data)


def reportes_globales_profesional(request):
    status = request_session_profesional(request)
    if (status == False):
        return redirect('getHome')

    data = {
        'session_status': request_session(request),
        'proyectos': get_capacitaciones(request),
        'clientes': get_all_clientes(request),
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
                    "id_capacitacion": capacitacion[i][0],
                    "nombre_capacitacion": capacitacion[i][2],
                })

            return data_to_array
    except Exception as ex:
        print(ex)


def insert_project(request):
    if (request.method == 'POST'):
        v_id = request.POST.get('numberCapacitacion')
        v_rut = request.session['profesional']['rut_usuario']
        if (v_id == ""):
            v_id = 0
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute("SELECT * FROM nma_capacitacion WHERE (id_capacitacion = %s and rut_usuario = '%s' )" % (v_id, v_rut))
                exist = cursor.fetchall()

                if (exist == ()):
                    v_nombreCapacitacion = request.POST.get(
                        'txtNombreCapacitacionProfesional')
                    v_descripcionCapacitacion = request.POST.get(
                        'txtDescripcionCapacitacionProfessional')
                    v_totalCapacitacion = request.POST.get(
                        'intTotalCapacitacion')
                    v_listStatus = request.POST.get('listStatusCapacitacion')
                    cursor.execute("""INSERT INTO nma_capacitacion (rut_usuario, nombre_capacitacion, descripcion_capacitacion, total_capacitacion, status_capacitaciones ) 
                                    VALUES ('%s', '%s', '%s', %s, %s)""" % (v_rut, v_nombreCapacitacion, v_descripcionCapacitacion, v_totalCapacitacion, v_listStatus))
                    cx.commit()
                else:
                    v_nombreCapacitacion = request.POST.get(
                        'txtNombreCapacitacionProfesional')
                    v_descripcionCapacitacion = request.POST.get(
                        'txtDescripcionCapacitacionProfessional')
                    v_totalCapacitacion = request.POST.get(
                        'intTotalCapacitacion')
                    v_listStatus = request.POST.get('listStatusCapacitacion')
                    cursor.execute("""UPDATE nma_capacitacion SET nombre_capacitacion = '%s',  descripcion_capacitacion = '%s',  total_capacitacion = %s,  status_capacitaciones = %s
                                    WHERE (id_capacitacion = %s AND rut_usuario = '%s') """ %
                                   (v_nombreCapacitacion, v_descripcionCapacitacion, v_totalCapacitacion, v_listStatus, v_id, v_rut))
                    cx.commit()
            cx.close()
            return redirect('projectsProfesional')
        except Exception as ex:
            print(ex)
            return redirect('projectsProfesional')
    else:
        return redirect('projectsProfesional')


def get_all_project_professional(request):
    v_rut = request.session['profesional']['rut_usuario']
    try:
        cx = get_connection()

        with cx.cursor() as cursor:
            cursor.execute("SELECT * FROM nma_capacitacion WHERE rut_usuario = '%s' " % (v_rut))
            datos = cursor.fetchall()

            data_to_array = []

            # A??ADIR HTML
            for i in datos:
                data_to_array.append({
                    'id_capacitacion': i[0],
                    'rut_usuario': i[1],
                    'nombre_capacitacion': i[2],
                    'descripcion_capacitacion': i[3],
                    'total_capacitacion': i[4],
                    'status_capacitacion': i[5],
                })
            
            # A??ADIR HTML
            for x in range(len(data_to_array)):
                data_to_array[x]['options'] = """
                    <div class="text-center">
                        <button type='button' class='btn btn-sm btn-success' onclick='fntViewActividades(%s)'
                            data-bs-toggle='modal' data-bs-target='#modalChecklist' style='background: linear-gradient(to right, deepskyblue, blueviolet);
                            border: none; border-radius: 3px !important;'>
                            <i class='bx bx-check-square' ></i>
                        </button>
                        <button type='button' class='btn btn-sm btn-primary' onclick='fntEditProject(%s)'
                            data-bs-toggle='modal' data-bs-target='#modalProject' style='background: linear-gradient(to right, deepskyblue, blueviolet);
                            border: none; border-radius: 3px !important;'>
                            <i class='bx bxs-edit' ></i>
                        </button>
                        <button onclick="fntConfirmDelete(%s)" class="btn btn-sm btn-danger" style='border-radius: 3px !important;'><i class='bx bx-trash'></i></button>
                    </div>
                """ % (data_to_array[x]['id_capacitacion'], data_to_array[x]['id_capacitacion'], data_to_array[x]['id_capacitacion'])

            return (data_to_array)
    except Exception as ex:
        print(ex)
        return redirect('projectsProfesional')


def delete_capacitacion(request):
    if (request.method == 'GET'):
        v_id = request.GET.get('numberCapacitacion')
        v_rut = request.session['profesional']['rut_usuario']
        if (v_id == ""):
            v_id = 0
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM nma_capacitacion WHERE (id_capacitacion = %s and rut_usuario = '%s' )" % (v_id, v_rut))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute(
                        "DELETE FROM nma_capacitacion WHERE (id_capacitacion = %s and rut_usuario = '%s' )" % (v_id, v_rut))
                    cx.commit()
            cx.close()
            return redirect('projectsProfesional')
        except Exception as ex:
            print(ex)
            return redirect('projectsProfesional')
    else:
        return redirect('projectsProfesional')


def get_capacitacion(request):
    if (request.method == 'GET'):
        v_id = request.GET.get('numberCapacitacion')
        v_rut = request.session['profesional']['rut_usuario']
        if (v_id == ""):
            v_id = 0
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM nma_capacitacion WHERE (id_capacitacion = %s and rut_usuario = '%s' )" % (v_id, v_rut))
                exist = cursor.fetchall()
                data_to_array = []
                """ nombre_capacitacion = '%s', 
                    descripcion_capacitacion = '%s', 
                    total_capacitacion = '%s', 
                    status_capacitaciones = '%s')  
                """
                if (exist != ()):
                    for i in exist:
                        data_to_array.append({
                            "id_capacitacion": i[0],
                            "rut_usuario": i[1],
                            "nombre_capacitacion": i[2],
                            "descripcion_capacitacion": i[3],
                            "total_capacitacion": i[4],
                            "status_capacitacion": i[5],
                        })
            cx.close()
            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as ex:
            print(ex)
            return redirect('projectsProfesional')
    else:
        return redirect('projectsProfesional')


def insert_reporteglobal(request):
    if (request.method == 'POST'):
        v_id = request.POST.get('folioReporte')
        v_rut_profesional = request.session['profesional']['rut_usuario']
        if (v_id == ""):
            v_id = 0
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute("""SELECT * FROM nma_reportes WHERE id = %s """ % (v_id))
                exist = cursor.fetchall()
                print(exist)
                if (exist == ()):
                    v_nombreReporte = request.POST.get('txtNombreReporte')
                    v_descripcionReporte = request.POST.get('txtDescripcionReporte')
                    v_fecha_utc = date.today()
                    v_rut_usuario = v_rut_profesional
                    v_rut_cliente = request.POST.get('listrutCliente')
                    v_idProyecto = request.POST.get('listProjects')
                    # print(v_rut_cliente)
                    cursor.execute(f"""
                        INSERT INTO nma_reportes (
                            nombre, descripcion, create_time, rut_cliente, rut_usuario, id_proyecto ) VALUES (
                            '{v_nombreReporte}', '{v_descripcionReporte}', '{v_fecha_utc}' , '{v_rut_cliente}', '{v_rut_usuario}', {v_idProyecto}  ) """)
                    cx.commit()
                    
                    reportePdf()

                else:
                    v_nombreReporte = request.POST.get('txtNombreReporte')
                    v_descripcionReporte = request.POST.get('txtDescripcionReporte')
                    v_fecha_utc = date.today()
                    v_rut_usuario = request.session['profesional']['rut_usuario']
                    v_rut_cliente = request.POST.get('listrutCliente')
                    v_idProyecto = request.POST.get('listProjects')
                    cursor.execute("""UPDATE nma_reportes SET nombre = '%s',  descripcion = '%s',  create_time = '%s',  rut_usuario = '%s' , rut_cliente = '%s' , id_proyecto = %s
                                WHERE (id = %s AND rut_usuario = '%s') """ %
                                (v_nombreReporte, v_descripcionReporte, v_fecha_utc, v_rut_usuario, v_rut_cliente, v_idProyecto, v_id, v_rut_usuario))
                    cx.commit()
            cx.close()
            return redirect('reportesGlobalesProfesional')
        except Exception as ex:
            print(ex)
            return redirect('reportesGlobalesProfesional')
    else:
        return redirect('reportesGlobalesProfesional')


def get_all_reportes_globales(request):
    v_rut = request.session['profesional']['rut_usuario']
    try:
        cx = get_connection()

        with cx.cursor() as cursor:
            cursor.execute("SELECT * FROM nma_reportes WHERE rut_usuario = '%s' " % (v_rut))
            datos = cursor.fetchall()

            data_to_array = []

            for i in datos:
                data_to_array.append({
                    'id': i[0],
                    'nombre': i[1],
                    'descripcion': i[2],
                    'create_time': i[3],
                    'rut_usuario': i[4],
                    'rut_cliente': i[5],
                    'id_proyecto': i[6],
                })

            for x in range(len(data_to_array)):
                data_to_array[x]['options'] = """
                    <div class="text-center" style='gap: 5px !important;'>
                        <a target="_blank" href="/profesional/api/v2/generate/pdf?idReporte=%s" class="btn btn-danger btn-sm" style='border-radius: 3px !important;'>PDF</a>
                        <button type='button' class='btn btn-sm btn-primary' onclick='fntEditReporte(%s)'
                            data-bs-toggle='modal' data-bs-target='#modalReporte' style='background: linear-gradient(to right, deepskyblue, blueviolet);
                            border: none; border-radius: 3px !important;'>
                            <i class='bx bxs-edit' ></i>
                        </button>
                        <button onclick="fntConfirmDelete(%s)" class="btn btn-sm btn-warning" style='border-radius: 3px !important;'><i class='bx bx-trash'></i></button>
                    </div>
                """ % (data_to_array[x]['id'], data_to_array[x]['id'], data_to_array[x]['id'])

            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
    except Exception as ex:
        print(ex)
        return redirect('reportesGlobalesProfesional')

def get_reportesGlobal(request):
    if (request.method == 'GET'):
        v_id = request.GET.get('idReporte')
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute("""SELECT * FROM nma_reportes WHERE id = '%s' """ % (v_id))
                data_reportes = cursor.fetchall()
                data_to_array = []

                for i in range(len(data_reportes)):
                    data_to_array.append({
                        "id": data_reportes[i][0],
                        "nombre": data_reportes[i][1],
                        "descripcion": data_reportes[i][2],
                        "create_time": data_reportes[i][3],
                        "rut_usuario": data_reportes[i][4],
                        "rut_cliente": data_reportes[i][5],
                        "id_proyecto": data_reportes[i][6],
                    })

                return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as ex:
            print(ex)
    else:
        return redirect('reportesGlobalesProfesional')

# DELETE CAPACITACI??N
def delete_reporte(request):
    if (request.method) == 'GET':
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_reporte = request.GET.get("idReporte")
                cursor.execute("""SELECT * FROM nma_reportes WHERE id = %s""" % (v_id_reporte))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute(
                        """DELETE FROM nma_reportes WHERE id = %s""" % (v_id_reporte))
                    cx.commit()
            cx.close()
            return redirect('reportesGlobalesProfesional')
        except Exception as ex:
            print(ex)
            return redirect('reportesGlobalesProfesional')
    else:
        messages.add_message(request, messages.ERROR,
                             'Ha ocurrido un error inesperado!')
        return redirect("reportesGlobalesProfesional")


def get_all_clientes(request):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("""SELECT rut_cliente, n1_cliente, ap_cliente, nombre_empresa FROM nma_cliente """)
            data_clientes = cursor.fetchall()
            data_to_array = []

            for i in range(len(data_clientes)):
                data_to_array.append({
                    "rut_cliente": data_clientes[i][0],
                    "n1_cliente": data_clientes[i][1],
                    "ap_cliente": data_clientes[i][2],
                    "nombre_empresa": data_clientes[i][3]
                })

            return (data_to_array)
    except Exception as ex:
        print(ex)


def getActividadProfesional(request):
    v_idCapacitacion = request.GET.get('idCapacitacion')
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute(f"""SELECT * FROM nma_actividad WHERE Id_capacitacion = {v_idCapacitacion}""")
            data_actividad = cursor.fetchall()

            data_to_array = []
            
            for i in data_actividad:
                data_to_array.append({
                    "id_actividad": i[0],
                    "nombre_actividad": i[2],
                    "descripcion_actividad": i[3],
                    "status_actividad": i[5]
                })

            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
    except Exception as ex:
        print(ex)
        return redirect('projectsProfesional')

def getAllActividadProfesional(request):
    v_idCapacitacion = request.GET.get('idCapacitacion')
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("""SELECT * FROM nma_actividad""")
            data_actividad = cursor.fetchall()

            data_to_array = []
            
            for i in data_actividad:
                data_to_array.append({
                    "id_actividad": i[0],
                    "nombre_actividad": i[2],
                    "descripcion_actividad": i[3],
                    "status_actividad": i[5]
                })

            # A??adir HTML}
            for i in data_to_array:
                if (i['status_actividad'] == 1):
                    i['status_actividad'] = """<div class='text-center'><button class='btn btn-sm btn-success' 
                        style='border: none;'>Finalizada</button></div>"""
                else:
                    i['status_actividad'] = """<div class='text-center'><button class='btn btn-sm btn-danger' 
                        style='border: none; color: white;'>Pendiente</button></div>"""

            # A??adir HTML
            for i in data_to_array:
                i['options'] = """
                    <div class='text-center'>
                        <a onclick='fntEnableActividad(%s)' class='btn btn-sm btn-success'><i class='bx bxs-check-circle' ></i></a>
                        <a onclick='fntDisableActividad(%s)' class='btn btn-sm btn-danger'><i class='bx bxs-x-circle' ></i></a>
                    </div>
                """ % (i['id_actividad'], i['id_actividad'])

            print("deberia emprimir en la tabla")
            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
    except Exception as ex:
        print(ex)
        print("jijijija")
        return redirect('projectsProfesional')


def enableActividadProfesional(request):
    if (request.method == "GET"):
        v_idActividad = request.GET.get("idActividad")
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute(f"SELECT * FROM nma_actividad WHERE id_actividad = {v_idActividad}")
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute(f"UPDATE nma_actividad SET status_actividad = 1 WHERE id_actividad = {v_idActividad}")
                    cx.commit()
                    return redirect("projectsProfesional")
                else:
                    return redirect("projectsProfesional")
        except Exception as ex:
            print(ex)
            return ('projectsProfesional')
    else:
        return redirect("projectsProfesional")


def disableActividadProfesional(request):
    if (request.method == "GET"):
        v_idActividad = request.GET.get("idActividad")
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute(f"SELECT * FROM nma_actividad WHERE id_actividad = {v_idActividad}")
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute(f"UPDATE nma_actividad SET status_actividad = 0 WHERE id_actividad = {v_idActividad}")
                    cx.commit()
                    return redirect("projectsProfesional")
                else:
                    return redirect("projectsProfesional")
        except Exception as ex:
            print(ex)
            return ('projectsProfesional')
    else:
        return redirect("projectsProfesional")



import os
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
import random

def reportePdf(request):
    if(request.method == 'GET'):
        v_id = request.GET.get('idReporte')

        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute(f"SELECT * FROM nma_reportes NMR JOIN nma_cliente NMC ON (NMR.rut_cliente = NMC.rut_cliente) WHERE NMR.id = {v_id}")
            exist = cursor.fetchall()
            data_to_array = []

            for i in exist:
                data_to_array.append({
                    'rut_cliente': i[5],
                    'rut_usuario': i[4],
                    'descripcion': i[2],
                    'n1_cliente': i[9],
                    'ap_cliente': i[11],
                    'nombre_empresa': i[16]
                })

            if(exist != ()):
                uuid =  str(random.randrange(100, 99999))
                template = get_template('modules/prueba-reporte.html')
                descripcion = data_to_array[0]['descripcion']
                cliente = data_to_array[0]['rut_cliente']
                nombre_cliente = data_to_array[0]['n1_cliente']
                apellido_cliente = data_to_array[0]['ap_cliente']
                usuario = data_to_array[0]['rut_usuario']
                empresa = data_to_array[0]['nombre_empresa']

                context = {
                    'title' : 'RSP Company Global Report',
                    'uuid': uuid,
                    'descripcion': descripcion,
                    'cliente': cliente,
                    'usuario': usuario,
                    'nombre_cliente': nombre_cliente,
                    'apellido_cliente': apellido_cliente,
                    'empresa': empresa,
                }
                
                html = template.render(context)
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename={uuid}.pdf'
                
                pisaStatus = pisa.CreatePDF(html, dest=response)
                
                if pisaStatus.err :
                    return HttpResponse("Error")
                
                return response
    else:
        return redirect('projectsProfesional')
    