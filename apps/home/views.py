from django.shortcuts import render, redirect
from django.conf import settings
import pymysql
import apps.core
import hashlib
from django.contrib import messages
from apps.helpers import *

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
                
                messages.add_message(request, messages.SUCCESS, '¡Bienvenido(a) ' + request.session["cliente"]["n1_cliente"] + ' ' + request.session["cliente"]["ap_cliente"] + ' de ' + request.session["cliente"]["nombre_empresa"] + ' !')
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
                
                messages.add_message(request, messages.SUCCESS, '¡Bienvenido(a) ' + request.session["profesional"]["primer_nombre"] + ' ' + request.session["profesional"]["apellido_paterno"] + ' !')
                return redirect ('index')
            else:
                messages.add_message(request, messages.ERROR, 'Usuario no Existente.')
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