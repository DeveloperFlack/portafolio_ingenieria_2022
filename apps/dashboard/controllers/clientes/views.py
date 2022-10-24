from genericpath import exists
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
                <button type='button' class='btn btn-sm btn-primary' onclick='fntEditCliente("%s")' 
                    data-bs-toggle='modal' data-bs-target='#modalEditClientes' style='background: linear-gradient(to right, deepskyblue, blueviolet);
                    border: none;'>
                    <i class='bx bxs-edit' ></i>                    
                </button>
                <a onclick='enableCliente(%s)' class='btn btn-sm btn-success'><i class='bx bx-power-off' ></i></a>
                <a onclick='disableCliente("%s")' class='btn btn-sm btn-warning'><i class='bx bx-power-off' ></i></a>
                <a onclick='deleteCliente("%s")' class='btn btn-sm btn-danger'><i class='bx bxs-trash-alt'></i></a>
            </div>
        """ % (i['rut_cliente'],i['rut_cliente'],i['rut_cliente'],i['rut_cliente'])

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

def dashboard_insert_cliente(request):
    """
    Si el método de solicitud es POST, entonces comprueba si el cliente existe, si no existe, entonces inserta el cliente,
    si existe, entonces actualiza el Cliente.

    :param request: El objeto de solicitud es un objeto HttpRequest
    :return: una redirección a la página getClientesPage.
    """
    if request.method == "POST":
        rut_cliente = request.POST.get("txtRut")
        exist = fc_get_cliente_dash(rut_cliente)
        if (exist == ()):
            # INSERTAR Cliente
            # v_contrasena_cliente = request.POST.get("txtContraseña") -> Por ahora no se utiliza ya que se genera la contraseña automáticamente en la variable "vaa"
            v_n1_cliente = request.POST.get("txtPrimerNombre")
            v_n2_cliente = request.POST.get("txtSegundoNombre")
            v_ap_cliente = request.POST.get("txtApellidoPaterno")
            v_am_cliente = request.POST.get("txtApellidoMaterno")
            v_correo_cliente = request.POST.get("txtCorreoElectronico")
            # Creating a hash of the second name, the @ symbol and the user's rut.
            vaa = v_n1_cliente + '@' + rut_cliente  # la contraseña corresponde al nombre del cliente + @ + rut
            v_password = hashlib.sha256(vaa.encode('utf-8')).hexdigest()
            
            v_telefono_cliente = request.POST.get("txtTelefono")
            v_rut_empresa_cliente = request.POST.get("txtRutEmpresa")
            v_nombre_empresa = request.POST.get("txtNombreEmpresa")
            v_status_Cliente = 0            

            fc_insert_cliente(rut_cliente, v_password, v_n1_cliente, v_n2_cliente, v_ap_cliente,
                v_am_cliente, v_correo_cliente, v_telefono_cliente, v_rut_empresa_cliente, v_nombre_empresa, v_status_Cliente)
            messages.add_message(request, messages.SUCCESS, 'Usuario ingresado Exitosamente!')
            return redirect("getClientesPage")

        else:
            # ACTUALIZAR Cliente
            exist = fc_get_cliente_dash(rut_cliente)
            if (exist != ()):
                v_rut_Cliente = request.POST.get("txtRut")
                v_contrasena_cliente = sha256(request.POST.get("txtContraseña"))
                v_n1_cliente = request.POST.get("txtPrimerNombre")
                v_n2_cliente = request.POST.get("txtSegundoNombre")
                v_ap_cliente = request.POST.get("txtApellidoPaterno")
                v_am_cliente = request.POST.get("txtApellidoMaterno")
                v_correo_cliente = request.POST.get("txtCorreoElectronico")
                
                v_telefono_cliente = request.POST.get("txtTelefono")
                v_rut_empresa_cliente = request.POST.get("txtDireccion")
                v_nombre_empresa = request.POST.get("txtDireccion")
                v_status_Cliente = 0                

                fc_update_cliente(v_rut_Cliente, v_contrasena_cliente, v_n1_cliente, v_n2_cliente,
                                  v_ap_cliente, v_am_cliente, v_telefono_cliente, v_rut_empresa_cliente, v_rut_empresa_cliente,v_nombre_empresa, v_status_Cliente)
                return redirect("getClientesPage")
            else:
                return redirect("getClientesPage")
    else:
        return redirect("getClientesPage")
def dashboard_delete_cliente(request):
    if request.method == "GET":
        v_rut_Cliente = request.GET.get("txtRut")
        exist = fc_get_cliente_dash(v_rut_Cliente)
        if (exist != ()):
            fc_delete_cliente(v_rut_Cliente)
            return redirect("getClientesPage")
        else:
            return redirect("getClientesPage")
    else:
        return redirect("getClientesPage")
