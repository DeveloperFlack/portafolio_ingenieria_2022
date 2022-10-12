from genericpath import exists
from symbol import try_stmt
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .usp import *
import pymysql
import hashlib
from apps.dashboard.controllers.roles.usp import fc_get_permisos
from django.contrib import messages
from apps.helpers import request_session


# Create your views here.
def getClientesPage(request):
    data = {
        'id' : 5,
        'meta_title': 'Dashboard - Clientes',
        'breadcrumb': "Clientes",
        'title': 'Lista de Clientes',
        'subtitle': 'Lista completa de Clientes del sistema',
        'button_add': 'Añadir Cliente',
    }
    a = helpers.session_user_exist(request)
    if (a == False):
        messages.add_message(request, messages.ERROR, 'No haz Iniciado Sesión.')
        return redirect ("loginDashboard")
    
    b = helpers.session_user_role(request)
    if (b == True):
        del request.session['usuario']
        messages.add_message(request, messages.ERROR, 'No tienes Permiso.')
        return redirect ("loginDashboard")
    
    c = helpers.request_module(request, data)
    if (c == True):
        return render(request, "clientes.html", data)

# OBTENER TODOS LOS CLIENTES
def getAllClientes(request):
    data_clientes = list(fc_get_all_clientes())
    data_to_array = []
    # Convertir TUPLA a Array Modificable
    for i in data_clientes:
        data_to_array.append({
            "rut_cliente": i[0],
            "contrasena_cliente": i[1],
            "n1_cliente": i[2],
            "n2_cliente": i[3],
            "ap_cliente": i[4],
            "am_cliente": i[5],
            "correo_cliente": i[6],
            "telefono_cliente": i[7],
            "rut_empresa_cliente": i[8],
            "nombre_empresa": i[9],
            "id_rol": i[10],
            "status_cliente": i[11],
        })

    for i in data_to_array:
        i['options'] = """
            <div class='text-center'>
                <button type='button' class='btn btn-sm btn-primary' onclick='fntEditCliente("%s")' data-bs-toggle='modal' data-bs-target='#modalEditClientes'><i class='bx bxs-edit' ></i></button>
            </div>
        """ % (i['rut_cliente'])

    return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})

# OBTENER UN CLIENTE
def dashboard_get_cliente(request):
    v_rut_cliente = request.GET.get('rutCliente')
    if (v_rut_cliente != ""):
        data_cliente = list(fc_get_cliente_dash(v_rut_cliente))
        data_to_array = []
        if (data_cliente != ()):
            for i in data_cliente:
                data_to_array.append({
                    "rut_cliente": i[0],
                    "contrasena_cliente": i[1],
                    "n1_cliente": i[2],
                    "n2_cliente": i[3],
                    "ap_cliente": i[4],
                    "am_cliente": i[5],
                    "correo_cliente": i[6],
                    "telefono_cliente": i[7],
                    "rut_empresa_cliente": i[8],
                    "nombre_empresa": i[9],
                })
            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return redirect("getClientesPage")
    else:
        return redirect("getClientesPage")

# UPDATE CLIENTE
def dashboard_update_cliente(request):
    if (request.method == 'POST'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_rut_cliente = request.POST.get("rutCliente")
                v_contrasena_cliente = request.POST.get("txtContrasenaCliente")
                v_correo_cliente = request.POST.get("txtCorreoCliente")
                v_telefono_cliente = request.POST.get("txtTelefonoCliente")
                v_nombre_empresa = request.POST.get("txtNombreEmpresaCliente")

                cursor.execute("SELECT * FROM nma_cliente WHERE rut_cliente = '%s'" % (v_rut_cliente))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("""UPDATE nma_cliente SET contrasena_cliente = '%s', 
                    correo_cliente = '%s', telefono_cliente = %s, nombre_empresa = '%s' WHERE rut_cliente = '%s' """ % 
                    (v_contrasena_cliente, v_correo_cliente, v_telefono_cliente, v_nombre_empresa, v_rut_cliente))

                    cx.commit()
                    return redirect("getClientesPage")

                else:
                    messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
                    return redirect("getClientesPage")

        except Exception as ex:
            # print(ex)
            messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
            return redirect("getClientesPage")
    else:
        return redirect("getClientesPage")