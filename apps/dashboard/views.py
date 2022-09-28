from django.shortcuts import render, redirect
import pymysql
import hashlib
import apps.helpers as helpers
from .usp import *
from django.conf import settings
from django.contrib import messages

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
        'Módulo' : "Dashboard"
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
            
            permisos = fc_get_permisos_with_modulos(request.session['usuario']['id_rol'])
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