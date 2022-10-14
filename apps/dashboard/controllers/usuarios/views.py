import base64
from fnmatch import translate
from hashlib import sha256
import re
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .usp import *
import hashlib
from cryptography.fernet import Fernet
import apps.helpers as helpers
from django.contrib import messages
from apps.dashboard.views import get_connection

"""
It returns a rendered template

:param request: El objeto de la solicitud
:return: Un diccionario con las claves: breadcrumb, title, subtitle, button_add
"""


def dashboard_get_usuarios_page(request):
    data = {
        'id': 4,
        'meta_title': 'Dashboard - Usuarios',
        'breadcrumb': "Usuarios",
        'title': 'Lista de Usuarios',
        'subtitle': 'Lista completa de usuarios',
        'button_add': 'Añadir nuevo usuario',
    }
    a = helpers.session_user_exist(request)
    if (a == False):
        messages.add_message(request, messages.ERROR,
                             'No haz Iniciado Sesión.')
        return redirect("loginDashboard")

    b = helpers.session_user_role(request)
    if (b == True):
        del request.session['usuario']
        messages.add_message(request, messages.ERROR, 'No tienes Permiso.')
        return redirect("loginDashboard")

    c = helpers.request_module(request, data)
    if (c == True):
        data['usuarios'] = dashboard_get_usuarios_all(request)
        data['roles'] = dashboard_get_roles(request)
        return render(request, "usuarios.html", data)


def dashboard_usuario_insert(request):
    """
    Si el método de solicitud es POST, entonces comprueba si el usuario existe, si no existe, entonces inserta el usuario,
    si existe, entonces actualiza el usuario.

    :param request: El objeto de solicitud es un objeto HttpRequest
    :return: una redirección a la página getUsuariosPage.
    """

    session_user = helpers.session_user_exist
    if (session_user == False):
        messages.add_message(request, messages.ERROR, 'No has Iniciado Sesión.')
        return redirect("loginDashboard")

    if request.method == "POST":
        v_rut_usuario = request.POST.get("txtRut")
        exist = fc_get_usuario(v_rut_usuario)
        if (exist == ()):
            # INSERTAR USUARIO
            v_primer_nombre = request.POST.get("txtPrimerNombre")
            v_segundo_nombre = request.POST.get("txtSegundoNombre")
            v_apellido_paterno = request.POST.get("txtApellidoPaterno")
            v_apellido_materno = request.POST.get("txtApellidoMaterno")
            v_correo = request.POST.get("txtCorreoElectronico")
            # Creating a hash of the second name, the @ symbol and the user's rut.
            vaa = v_primer_nombre + '@' + v_rut_usuario

            v_password = hashlib.sha256(vaa.encode('utf-8')).hexdigest()
            v_telefono = request.POST.get("txtTelefono")
            v_direccion = request.POST.get("txtDireccion")
            v_status_usuario = 0
            v_id_rol = int(request.POST.get("selectRol"))

            fc_insert_usuario(v_rut_usuario, v_primer_nombre, v_segundo_nombre, v_apellido_paterno, v_apellido_materno, v_correo, v_password, v_telefono, v_direccion, v_status_usuario, v_id_rol)

            return redirect("getUsuariosPage")

        else:
            # ACTUALIZAR USUARIO
            exist = fc_get_usuario(v_rut_usuario)
            if (exist != ()):
                v_rut_usuario = request.POST.get("txtRut")
                v_primer_nombre = request.POST.get("txtPrimerNombre")
                v_segundo_nombre = request.POST.get("txtSegundoNombre")
                v_apellido_paterno = request.POST.get("txtApellidoPaterno")
                v_apellido_materno = request.POST.get("txtApellidoMaterno")
                v_correo = request.POST.get("txtCorreoElectronico")
                
                vaa = v_primer_nombre + '@' + v_rut_usuario
                v_password = hashlib.sha256(vaa.encode('utf-8')).hexdigest()    
                    
                v_telefono = request.POST.get("txtTelefono")
                v_direccion = request.POST.get("txtDireccion")
                v_status_usuario = 0
                v_id_rol = int(request.POST.get("selectRol"))

                fc_update_usuario(v_rut_usuario, v_primer_nombre, v_segundo_nombre, v_apellido_paterno, v_apellido_materno, v_correo, v_password, v_telefono, v_direccion, v_status_usuario, v_id_rol)
                return redirect("getUsuariosPage")
            else:
                return redirect("getUsuariosPage")
    else:
        return redirect("getUsuariosPage")


def dashboard_get_usuarios_all(request):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute(
                "SELECT rut_usuario, primer_nombre, apellido_paterno, direccion, correo, status_usuario, nombre_rol FROM nma_usuario nmu join nma_roles nmr on(nmu.id_rol = nmr.id_rol)")
            data = cursor.fetchall()

            data_to_array = []
            for i in range(len(data)):
                data_to_array.append(
                    {
                        "rut_usuario": data[i][0],
                        "primer_nombre": data[i][1],
                        "apellido_paterno": data[i][2],
                        "direccion": data[i][3],
                        "correo": data[i][4],
                        "status_usuario": data[i][5],
                        "nombre_rol": data[i][6]
                    }
                )
            for i in range (len(data_to_array)):
                if (data_to_array[i]['status_usuario'] == 1):
                    data_to_array[i]['status_usuario']  = """<div class='text-center'><button class='btn btn-sm btn-success' 
                        style='background: linear-gradient(to right, deepskyblue, blueviolet); border: none;'>Activado</button></div>"""
                else:
                    data_to_array[i]['status_usuario']  = """<div class='text-center'><button class='btn btn-sm btn-danger' 
                        style='background: linear-gradient(to right, orange, deeppink); border: none; color: white;'>Desactivado</button></div>"""
                    
                data_to_array[i]['options'] = """
                    <div class='text-center'>
                        <button type='button' class='btn btn-sm btn-primary' onclick='fntEditUsuario("%s")' 
                            data-bs-toggle='modal' data-bs-target='#modalUsuario' style='background: linear-gradient(to right, deepskyblue, blueviolet);
                            border: none;'>
                            <i class='bx bxs-edit' ></i>
                        </button>
                        <a onclick='enableUsuario("%s")' class='btn btn-sm btn-success'><i class='bx bx-power-off' ></i></a>
                        <a onclick='disableUsuario("%s")' class='btn btn-sm btn-warning'><i class='bx bx-power-off' ></i></a>
                        <a onclick='fntConfirmDelete("%s")' class='btn btn-sm btn-danger'><i class='bx bxs-trash-alt'></i></a>
                    </div>
                """ % (data_to_array[i]['rut_usuario'], data_to_array[i]['rut_usuario'], data_to_array[i]['rut_usuario'], data_to_array[i]['rut_usuario'])
            return data_to_array
    except Exception as ex:
        print(ex)
        return redirect("getUsuariosPage")


def dashboard_get_user(request):
    session_user = helpers.session_user_exist
    if (session_user == False):
        messages.add_message(request, messages.ERROR,
                             'No has Iniciado Sesión.')
        return redirect("loginDashboard")

    if (request.method == "GET"):
        v_rut_usuario = request.GET.get('idUsuario')

        data_user = fc_get_usuario(v_rut_usuario)

        if (data_user != ()):
            for i in data_user:
                data_to_array = {
                    "rut_usuario": i[0],
                    "primer_nombre": i[1],
                    "segundo_nombre": i[2],
                    "apellido_paterno": i[3],
                    "apellido_materno": i[4],
                    "correo": i[5],
                    "password_usuario": i[6],
                    "telefono": i[7],
                    "direccion": i[8],
                    "status_usuario": i[9],
                    "id_rol": i[10],
                }
            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return redirect("getUsuariosPage")
    else:
        return redirect("getUsuariosPage")


def dashboard_disable_user(request):
    if (request.method == 'GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_rutUsuario = request.GET.get('idUsuario')
                cursor.execute("SELECT * FROM nma_usuario WHERE rut_usuario = '%s'" % (v_rutUsuario))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("UPDATE nma_usuario SET status_usuario = 0 WHERE rut_usuario = '%s'" % (v_rutUsuario))
                    cx.commit()
                    return redirect("getUsuariosPage")
                else:
                    messages.add_message(request, messages.ERROR, 'Error.')
                    return redirect("getUsuariosPage")
        except Exception as ex:
            print(ex)
            return redirect("getUsuariosPage")
    else:
        return redirect("getUsuariosPage")


def dashboard_enable_user(request):
    if (request.method == 'GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_rutUsuario = request.GET.get('idUsuario')
                cursor.execute(
                    "SELECT * FROM nma_usuario WHERE rut_usuario = '%s'" % (v_rutUsuario))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute(
                        "UPDATE nma_usuario SET status_usuario = 1 WHERE rut_usuario = '%s'" % (v_rutUsuario))
                    cx.commit()
                    return redirect("getUsuariosPage")
                else:
                    messages.add_message(request, messages.ERROR, 'Error.')
                    return redirect("getUsuariosPage")
        except Exception as ex:
            print(ex)
            return redirect("getUsuariosPage")
    else:
        return redirect("getUsuariosPage")


def dashboard_delete_user(request):
    if (request.method == 'GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_rutUsuario = request.GET.get('idUsuario')
                cursor.execute(
                    "SELECT * FROM nma_usuario WHERE rut_usuario = '%s'" % (v_rutUsuario))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute(
                        "DELETE FROM nma_usuario WHERE rut_usuario = '%s'" % (v_rutUsuario))
                    cx.commit()
                    return redirect("getUsuariosPage")
                else:
                    messages.add_message(request, messages.ERROR, 'Error.')
                    return redirect("getUsuariosPage")
        except Exception as ex:
            print(ex)
            return redirect("getUsuariosPage")
    else:
        return redirect("getUsuariosPage")

def dashboard_get_roles(request):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute('SELECT * FROM nma_roles WHERE id_rol != 2')
            roles = cursor.fetchall()
            data_to_array = []
            
            for i in range(len(roles)):
                data_to_array.append({
                    "id_rol" : roles[i][0],
                    "nombre_rol" : roles[i][1],
                })
            
            return data_to_array
    except Exception as ex:
        print (ex)