from django.shortcuts import render, redirect
from django.http import HttpResponse
import pymysql
import hashlib
import apps.helpers as helpers
from .usp import *
from django.conf import settings
from django.contrib import messages
import math
import json

# Tupla = (1,2,3,4,5,6,7,8)
# Array = []
# Diccionario = {}
def multiform(form):
    """
    Toma un diccionario de la forma {'a[b][c]': 'd', 'e[f][g]': 'h'} y devuelve {'a': {'b': {' c':
    'd'}}, 'e': {'f': {'g': 'h'}}}
    
    :param form: Los datos del formulario que desea convertir en un diccionario
    """
    data = {}
    for url_k in form:
        v = form[url_k]
        ks = []
        while url_k:
            if '[' in url_k:
                k, r = url_k.split('[', 1)
                ks.append(k)
                if r[0] == ']':
                    ks.append('')
                url_k = r.replace(']', '', 1)
            else:
                ks.append(url_k)
                break
        sub_data = data
        for i, k in enumerate(ks):
            if k.isdigit():
                k = int(k)
            if i+1 < len(ks):
                if not isinstance(sub_data, dict):
                    break
                if k in sub_data:
                    sub_data = sub_data[k]
                else:
                    sub_data[k] = {}
                    sub_data = sub_data[k]
            else:
                if isinstance(sub_data, dict):
                    sub_data[k] = v
    return data

def get_connection ():
    return pymysql.connect (host=settings.DB_HOST, database=settings.DB_SCHEMA, user=settings.DB_USER, password=settings.DB_PASS)

def getDashboard (request):
    data = {
        'id' : 1,
        'Módulo' : "Dashboard",
        'percentage_da_services': get_count_asesorias(request),
        'capacitaciones': get_count_capacitaciones(request),
        'solicitudes': get_count_solicitudes(request),
        'percentage_profesional': get_count_profesionales(request),
        'clientes': get_count_clientes(request),
        'accidentes': get_count_accidentes(request),
    }
    
    a = helpers.session_user_exist(request)
    if (a == False):
        messages.add_message(request, messages.ERROR, 'No has Iniciado Sesión.')
        return redirect ("loginDashboard")
    
    b = helpers.session_user_role(request)
    if (b == True):
        del request.session['usuario']
        messages.add_message(request, messages.ERROR, 'No tienes Permiso.')
        return redirect ("loginDashboard")
    
    c = helpers.request_module(request, data)
    if (c == True):
        return render(request, "dashboard.html", data)


def loginDashboard (request):
    data = {
        'meta_title' : 'Dashboard - Login'
    }
    
    x = 'usuario' in request.session
    
    if (x == True):
        return redirect ("principalDashboard")

    return render (request, "login.html", data)

def loginAdministrador (request):
    if request.method == "POST":
        
        v_rut_usuario =  request.POST.get("txtRutUsuario")
        if (v_rut_usuario == ""):
            messages.success(request, 'Profile details updated.')
            return redirect ("loginDashboard")
        v_c = request.POST.get("txtContraseñaUsuario")
        v_contraseña_usuario = hashlib.sha256((v_c).encode('utf-8')).hexdigest()

        exists = fc_user_login(v_rut_usuario, v_contraseña_usuario)
        # type(exists)

        if (exists != ()):
            data_to_array = []
            for x in exists:
                data_to_array.append({
                    "RUT" : x[0],
                    "primer_nombre" : x[1],
                    "segundo_nombre" : x[2],
                    "apellido_paterno" : x[3],
                    "apellido_materno" : x[4],
                    "correo" : x[5],
                    "password_usuario" : x[6],
                    "telefono" : x[7],
                    "direccion" : x[8],
                    "status_usuario" : x[9],
                    "id_rol" : x[10],
                })
            request.session["usuario"] = {
                'RUT' : data_to_array[0]["RUT"],
                "primer_nombre" : data_to_array[0]["primer_nombre"],
                "segundo_nombre" : data_to_array[0]["segundo_nombre"],
                "apellido_paterno" : data_to_array[0]["apellido_paterno"],
                "apellido_materno" : data_to_array[0]["apellido_materno"],
                "correo" : data_to_array[0]["correo"],
                "password_usuario" : data_to_array[0]["password_usuario"],
                "telefono" : data_to_array[0]["telefono"],
                "direccion" : data_to_array[0]["direccion"],
                "status_usuario" : data_to_array[0]["status_usuario"],
                "id_rol" : data_to_array[0]["id_rol"],
            }
            
            permisos = fc_get_permisos_with_modulos_1(request.session['usuario']['id_rol'])
            data_to_array_permisos = []
            for x in permisos:
                data_to_array_permisos.append({
                    'id_modulo' : x[0],
                    'nombre_modulo' : x[1],
                    'create' : x[2],
                    'read' : x[3],
                    'update' : x[4],
                    'delete' : x[5],
                })
            request.session['usuario']['permisos'] = data_to_array_permisos
            return redirect ('principalDashboard')
        else:
            return redirect ("loginDashboard")
    else:
        return redirect ("loginDashboard")

def logoutAdm(request):
    try:
        del request.session['usuario']
        del request.session['hola']
        print (request.session.items())
        return redirect('loginDashboard')
    except KeyError:
        print (request.session.items())
        return redirect('loginDashboard')

def get_count_asesorias(request):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("""SELECT COUNT(id_asesoria) FROM nma_asesoria WHERE status_asesoria != 0 """)
            as_active_1 = cursor.fetchall()
            
            cursor.execute("""SELECT COUNT(id_asesoria) FROM nma_asesoria""")
            as_total = cursor.fetchall()

            x = (as_active_1[0][0] / as_total[0][0] ) * 100
            data =  {
                'activas' : as_active_1[0][0],
                'total' : as_total[0][0],
                'porcentaje' : math.trunc(x)
                }
            return data
    except Exception as ex:
        print(ex)

def get_count_capacitaciones(request):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute(""" 
                SELECT COUNT(id_capacitacion)
                FROM nma_capacitacion 
                WHERE status_capacitaciones != 0
            """)
            capacitaciones = cursor.fetchall()
            data_to_array = []
        
            for i in range(len(capacitaciones)):
                data_to_array.append({
                    "count_id": capacitaciones[i][0]
                })

            return data_to_array
    except Exception as ex:
        print(ex)

def get_count_solicitudes(request):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute(""" 
                SELECT COUNT(id_solicitud)
                FROM nma_solicitudes 
                WHERE status_solicitud != 0
            """)
            solicitudes = cursor.fetchall()
            data_to_array = []
        
            for i in range(len(solicitudes)):
                data_to_array.append({
                    "count_id": solicitudes[i][0]
                })

            return data_to_array
    except Exception as ex:
        print(ex)

def get_count_profesionales(request):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute(""" 
                SELECT COUNT(rut_usuario)
                    FROM nma_usuario
                WHERE status_usuario != 0
            """)
            status_1 = cursor.fetchall()
            
            cursor.execute("""SELECT COUNT(rut_usuario) FROM nma_usuario """)
            pro_total = cursor.fetchall()
            
            x = (status_1[0][0] / pro_total[0][0]) * 100
            
            data =  {
                'activas' : status_1[0][0],
                'total' : pro_total[0][0],
                'porcentaje' : math.trunc(x)
                }
            
            return data
    except Exception as ex:
        print(ex)

def get_count_clientes(request):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute(""" 
                SELECT COUNT(rut_cliente)
                FROM nma_cliente
            """)
            clientes = cursor.fetchall()
            data_to_array = []
        
            for i in range(len(clientes)):
                data_to_array.append({
                    "count_rut": clientes[i][0],
                    "status_cliente": clientes[i][11]
                })

            return data_to_array
    except Exception as ex:
        print(ex)

def get_count_accidentes(request):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute(""" 
                SELECT COUNT(id_accidente)
                FROM nma_accidentes
            """)
            accidente = cursor.fetchall()
            data_to_array = []
        
            for i in range(len(accidente)):
                data_to_array.append({
                    "count_id": accidente[i][0]
                })

            return data_to_array
    except Exception as ex:
        print(ex)
        
def get_stadistics (request):
    try:
        cx = get_connection()
        
        with cx.cursor() as cursor :
            """ CPC = CAPACITACIONES """
            cursor.execute("SELECT * FROM nma_capacitacion")
            data_cpc= cursor.fetchall()
            array_cpc = []
            
            for x in data_cpc :
                array_cpc.append({
                    'id' : x[0],
                    'rut' : x[1],
                    'nombre' : x[2],
                    'descripcion' : x[3],
                    'total' : x[4],
                    'status' : x[5],
                })

            cursor.execute("SELECT * FROM nma_asesoria")
            data_ass = cursor.fetchall()
            array_ass = []

            for x in data_ass :
                array_ass.append({
                    'id' : x[0],
                    'rut' : x[1],
                    'nombre' : x[2],
                    'descripcion' : x[3],
                    'total' : x[4],
                    'status' : x[5],
                })

            cursor.execute("SELECT * FROM nma_solicitudes")
            data_sol = cursor.fetchall()
            array_sol = []

            for i in data_sol :
                array_sol.append({
                    "id_solicitud": i[0],
                    "rut_cliente": i[1],
                    "nombre_solicitud": i[4],
                    "descripcion_solicitud": i[5],
                    "tipo_solicitud": i[6],
                    "status_solicitud": i[11],
                    'fecha': i[7],
                    'time_start': i[8],
                    'time_end': i[9]
                })

            cursor.execute("SELECT * FROM nma_cliente")
            data_cli = cursor.fetchall()
            array_cli = []

            for i in data_cli :
                array_cli.append({
                    "rut_cliente": i[0],
                    "status_cliente": i[11]
                })

            cursor.execute("SELECT * FROM nma_accidentes")
            data_acci = cursor.fetchall()
            array_acci = []

            for i in data_acci :
                array_acci.append({
                    "id_accidente": i[0],
                    "status_accidente": i[7]
                })
            
            cursor.execute("SELECT * FROM nma_usuario")
            data_pro = cursor.fetchall()
            array_pro = []

            for i in data_pro :
                array_pro.append({
                    "rut": i[0],
                    "status" : i[9]
                })
                
            data = {
                'capacitaciones' : array_cpc,
                'asesorias' : array_ass,
                'solicitudes' : array_sol,
                'clientes' : array_cli,
                'profesionales' : array_pro,
                'accidentes' : array_acci
            }
            return HttpResponse(json.dumps(data,ensure_ascii=False, default=str), content_type='application/json; charset=utf-8; lang=es')
    except Exception as ex:
        print (ex)