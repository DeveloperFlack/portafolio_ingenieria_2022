from django.shortcuts import render, redirect
from django.conf import settings
import pymysql
import apps.core
import hashlib
from django.contrib import messages
from apps.helpers import *
from apps.home.controllers.cliente.usp import *
import js2py
from django.http import HttpResponse

def multiform(form):
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

def getHome(request):
    
    sessionStatus = request_session(request)
    data = {
        'capacitaciones_index' : get_capacitaciones_index(request),
        'session_status' : sessionStatus
    }
    return render(request, "index.html", data)

def auth (request):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            v_rut_usuario = request.POST.get("txtRut")
            vaa = request.POST.get("txtPassword")
            v_password_usuario = hashlib.sha256(vaa.encode('utf-8')).hexdigest()
            
            cursor.execute("select * from nma_cliente where rut_cliente = '%s' and contrasena_cliente = '%s'" % (v_rut_usuario, v_password_usuario))
            cliente = cursor.fetchall()
            
            cursor.execute("select * from nma_usuario where rut_usuario = '%s' and password_usuario = '%s'" % (v_rut_usuario, v_password_usuario))
            profesional = cursor.fetchall()
            
            if (cliente != ()):
                data_to_array = []
                for x in cliente:
                    data_to_array.append({
                        "rut_cliente" : x[0],
                        "rut_empresa_cliente" : x[8],
                        "contrasena_cliente" : x[1],
                        "n1_cliente" : x[2],
                        "ap_cliente" : x[4],
                        "nombre_empresa": x[9],
                    })
                request.session["cliente"] = {
                    "rut_cliente" : data_to_array[0]["rut_cliente"],
                    "rut_empresa_cliente" : data_to_array[0]["rut_empresa_cliente"],
                    "contrasena_cliente" : data_to_array[0]["contrasena_cliente"],
                    "n1_cliente": data_to_array[0]["n1_cliente"],
                    "ap_cliente": data_to_array[0]["ap_cliente"],
                    "nombre_empresa": data_to_array[0]["nombre_empresa"],
                }
                
                # messages.add_message(request, messages.SUCCESS, '¡Bienvenido(a) ' + request.session["cliente"]["n1_cliente"] + ' ' + request.session["cliente"]["ap_cliente"] + ' de ' + request.session["cliente"]["nombre_empresa"] + ' !'
                
                return redirect ('index')

            elif (profesional != ()):

                data_to_array = []
                for x in profesional:
                    data_to_array.append({
                        "rut_usuario" : x[0],
                        "primer_nombre" : x[1],
                        "apellido_paterno" : x[3],
                        "password_usuario" : x[6],
                    })
                request.session["profesional"] = {
                    "rut_usuario" : data_to_array[0]["rut_usuario"],
                    "primer_nombre" : data_to_array[0]["primer_nombre"],
                    "apellido_paterno" : data_to_array[0]["apellido_paterno"],
                    "password_usuario": data_to_array[0]["password_usuario"],
                }
                
                # messages.add_message(request, messages.SUCCESS, '¡Bienvenido(a) ' + request.session["profesional"]["primer_nombre"] + ' ' + request.session["profesional"]["apellido_paterno"] + ' !')
                return redirect ('index')
            
            else:
                # messages.add_message(request, messages.ERROR, 'Usuario no Existente.')

                return redirect ('index')

    except Exception as ex:
        messages.add_message(request, messages.SUCCESS, ex)
        return redirect ('index')
    
def logout(request):
    try:
        sessionStatus = request_session(request)
        if (sessionStatus['cliente'] == True):
            del request.session['cliente']
            return redirect('getHome')
        elif (sessionStatus['profesional'] == True):
            del request.session['profesional']
            return redirect('getHome')
        else:
            messages.add_message(request, messages.ERROR, "No se ha encontrado Sesión")
            return redirect('getHome')
    except KeyError:
        return redirect('index')

def register_cliente(request):
    if request.method == "POST":
        v_rut_cliente = request.POST.get("txtRutCliente")
        exist = fc_get_cliente(v_rut_cliente)
        if (exist == ()):
            # INSERTAR CLIENTE
            v_rut_empresa = request.POST.get("txtRutEmpresa")
            v_n1_cliente = request.POST.get("txtN1Cliente")
            v_n2_cliente = request.POST.get("txtN2Cliente")
            v_ap_cliente = request.POST.get("txtApellidoPaternoCliente")
            v_am_cliente = request.POST.get("txtApellidoMaternoCliente")
            v_correo_cliente = request.POST.get("txtCorreoCliente")
            v_contacto_cliente = request.POST.get("txtContactoCliente")
            v_nombre_empresa = request.POST.get("txtNombreEmpresa")
            vaa = request.POST.get("txtPasswordCliente")

            v_password_cliente = hashlib.sha256(vaa.encode('utf-8')).hexdigest()
            
            v_id_rol = 2
            v_status_cliente = 1

            fc_home_register(
                v_rut_cliente, v_password_cliente, v_n1_cliente, v_n2_cliente, v_ap_cliente, v_am_cliente, 
                v_correo_cliente, v_contacto_cliente, v_rut_empresa, v_nombre_empresa, v_id_rol, v_status_cliente
            )
            # print (urls.urlpatterns[0])
            return redirect("getHome")

        else:
            messages.add_message(request, messages.ERROR, "Usuario ya existente")
            return redirect("getHome")
    else:
        return redirect("getHome")

def get_capacitaciones_index(request):
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
                    "descripcion_capacitacion" : capacitacion[i][3],
                    "total_capacitacion" : capacitacion[i][4],
                })
            
            return data_to_array
    except Exception as ex:
        print (ex)