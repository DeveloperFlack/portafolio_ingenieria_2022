from django.shortcuts import render, redirect
from django.http import JsonResponse
from .usp import *
import apps.helpers as helpers
from django.http import HttpResponse


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




def getAllClients(request):
    return HttpResponse("Salida")

def getAllClientes(request):
    data_clientes = list(fc_get_all_clientes())
    data_to_array = []
    # Convertir TUPLA a Array Modificable
    for i in data_clientes:
        data_to_array.append({
            "rut_cliente": i[0],
            "n1_cliente": i[2],
            "n2_cliente": i[3],
            "ap_cliente": i[4],
            "am_cliente": i[5],
            "correo_cliente": i[6],
            "telefono_cliente": i[7],
            "rut_empresa_cliente": i[8],
            "nombre_empresa": i[9],
        })

    print(data_clientes)
    print(' - ')
    print(data_to_array)
    # Añadir HTML
    for i in data_to_array:
        i['options'] = """
            <div class='text-center'>
                <button type='button' class='btn btn-sm btn-primary' onclick='fntEditCLiente("%s")' data-bs-toggle='modal' data-bs-target='#modalCLiente'><i class='bx bxs-edit' ></i></button>
            </div>
        """ % (i['n1_cliente'])

    return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})