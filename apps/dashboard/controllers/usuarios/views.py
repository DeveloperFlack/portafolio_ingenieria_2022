import base64
from fnmatch import translate
from hashlib import sha256
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .usp import *
import hashlib
from cryptography.fernet import Fernet

"""
It returns a rendered template

:param request: El objeto de la solicitud
:return: Un diccionario con las claves: breadcrumb, title, subtitle, button_add
"""
def getUsuariosPage(request):
    data = {
        'meta_title' : 'Dashboard - Usuarios',
        'breadcrumb': "Usuarios",
        'title': 'Lista de Usuarios',
        'subtitle': 'Lista completa de usuarios',
        'button_add': 'Añadir Usuario',
    }

    return render(request, "usuarios.html", data)

def insertUsuario(request):
    """
    Si el método de solicitud es POST, entonces comprueba si el usuario existe, si no existe, entonces inserta el usuario,
    si existe, entonces actualiza el usuario.
    
    :param request: El objeto de solicitud es un objeto HttpRequest
    :return: una redirección a la página getUsuariosPage.
    """
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
            vaa = v_primer_nombre+ '@' +v_rut_usuario

            v_password = hashlib.sha256(vaa.encode('utf-8')).hexdigest()
            v_telefono = request.POST.get("txtTelefono")
            v_direccion = request.POST.get("txtDireccion")
            v_status_usuario = 0
            v_id_rol = int(request.POST.get("selectRol"))

            fc_insert_usuario(v_rut_usuario,v_primer_nombre,v_segundo_nombre,v_apellido_paterno,v_apellido_materno,v_correo,v_password,v_telefono,v_direccion,v_status_usuario,v_id_rol)

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
                v_password = sha256(request.POST.get("txtContraseña"))
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

def getAllUsuarios(request):
    """
    Toma una tupla de tuplas y la convierte en una lista de diccionarios
    
    :param request: El objeto de la solicitud
    :return: [{'rut_usuario': '17.876.876-8', 'primer_nombre': 'Juan', 'segundo_nombre': 'Andres',
    'apellido_paterno': 'Perez', 'apellido_materno': 'Gonzalez', 'correo
    """
    data_ususarios = list(fc_get_all_usuarios())
    data_to_array = []
    # Convertir TUPLA a Array Modificable
    for i in data_ususarios:
        data_to_array.append({
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
        })
    # sha256(as_bytestring(s)).hexdigest().decode('ascii')
    p1 = 'hoa'
    v1 = hashlib.sha256(p1.encode('utf-8')).hexdigest()
    print (v1)

    hashlib.sha256(v1.decode('utf-8'))

    # Añadir HTML
    for i in data_to_array:
        if (i['status_usuario'] == 1):
            i['status_usuario'] = "<div class='text-center'><button class='btn btn-success'>Activado</button></div>"
        else:
            i['status_usuario'] = "<div class='text-center'><button class='btn btn-warning'>Desactivado</button></div>"
        
        i['options'] = """
            <div class='text-center'>
                <button type='button' class='btn btn-sm btn-primary' onclick='fntEditUsuario("%s")' data-bs-toggle='modal' data-bs-target='#modalUsuarios'><i class='bx bxs-edit' ></i></button>
                <a onclick='enableUsuario(%s)' class='btn btn-sm btn-success'><i class='bx bx-power-off' ></i></a>
                <a onclick='disableUsuario("%s")' class='btn btn-sm btn-warning'><i class='bx bx-power-off' ></i></a>
                <a onclick='deleteUsuario("%s")' class='btn btn-sm btn-danger'><i class='bx bxs-trash-alt'></i></a>
            </div>
        """ % (i['rut_usuario'], i['rut_usuario'], i['rut_usuario'], i['rut_usuario'])

    return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
