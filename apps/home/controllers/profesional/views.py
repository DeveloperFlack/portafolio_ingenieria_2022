from genericpath import exists
from django.shortcuts import render, redirect
from django.conf import settings
import pymysql
import hashlib
from apps.dashboard.controllers.roles.usp import fc_get_permisos

# Create your views here.

def loginDahboard (request):
    if request.method == "POST":
        v_rut_usuario =  request.POST.get("txtRutClient")
        v_c = request.POST.get("txtPasswordClient")
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
            return redirect ('principalDashboard')
        else:
            return redirect ("loginDashboard")
    else:
        return redirect ("loginDashboard")