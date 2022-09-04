from django.shortcuts import render, redirect
from django.http import JsonResponse
from .usp import *

    
def getModulosPage(request):
    """
    Representa la plantilla modulos.html y le pasa el diccionario de datos
    
    :param request: El objeto de la solicitud
    :return: Un diccionario con las claves: breadcrumb, title, subtitle, button_add
    """

    data = {
        'meta_title' : 'Dashboard - Módulos',
        'breadcrumb': "Módulos",
        'title': 'Lista de Módulos',
        'subtitle': 'Lista completa de módulos',
        'button_add': 'Añadir Módulo',
    }

    return render(request, "modulos.html", data)

def insertModulo(request):
    """
    Si el método de solicitud es POST, entonces comprueba si el idModulo está vacío. Si lo está, entonces inserta un nuevo
    módulo. Si no lo está, entonces actualiza el módulo.
    
    :param request: The request object is an HttpRequest object. It contains metadata about the request,
    including the HTTP method
    :return: the redirect function.
    """
    if request.method == "POST":
        v_idModulo = request.POST.get("idModulo")
        if (v_idModulo == ""):
            # INSERTAR MÓDULO
            # Obtener los datos del formulario e insertarlos en la base de datos.
            v_nombre_modulo = request.POST.get("txtNombreModulo")
            v_descripcionModulo = request.POST.get("txtDescripcionModulo")
            fc_insert_module(v_nombre_modulo, v_descripcionModulo)
            return redirect("getModulosPage")

        else:
            # ACTUALIZAR MODULO
            # Verificando si el módulo existe, si existe, actualiza el módulo, si no, redirige a
            # getModulosPage.
            exist = fc_get_module(v_idModulo)
            if (exist != ()):
                v_nombre_modulo = request.POST.get("txtNombreModulo")
                v_descripcionModulo = request.POST.get("txtDescripcionModulo")
                fc_update_module(v_idModulo, v_nombre_modulo, v_descripcionModulo)
                return redirect("getModulosPage")
            else:
                return redirect("getModulosPage")

    else:
        return redirect("getModulosPage")

def getAllModulos(request):
    data_modulos = list(fc_get_all_modules())
    data_to_array = []
    # Convertir TUPLA a Array Modificable
    for i in data_modulos:
        data_to_array.append({
            "id_modulo": i[0],
            "nombre_modulo": i[1],
            "descripcion_modulo": i[2],
            "status_modulo": i[3],
        })

    # Añadir HTML
    for i in data_to_array:
        if (i['status_modulo'] == 1):
            i['status_modulo'] = "<div class='text-center'><button class='btn btn-success'>Activado</button></div>"
        else:
            i['status_modulo'] = "<div class='text-center'><button class='btn btn-warning'>Desactivado</button></div>"
        
        i['options'] = """
            <div class='text-center'>
                <button type='button' class='btn btn-sm btn-primary' onclick='fntEditModule("%s")' data-bs-toggle='modal' data-bs-target='#modalModulos'><i class='bx bxs-edit' ></i></button>
                <a onclick='enableModule(%s)' class='btn btn-sm btn-success'><i class='bx bx-power-off' ></i></a>
                <a onclick='disableModule("%s")' class='btn btn-sm btn-warning'><i class='bx bx-power-off' ></i></a>
                <a onclick='deleteModule("%s")' class='btn btn-sm btn-danger'><i class='bx bxs-trash-alt'></i></a>
            </div>
        """ % (i['id_modulo'], i['id_modulo'], i['id_modulo'], i['id_modulo'])

    return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})

def getModulo(request):
    """
    Obtiene la identificación del módulo y devuelve los datos del módulo en formato JSON.
    
    :param request: El objeto de solicitud es un objeto HttpRequest
    :return: Una lista de diccionarios.
    """
    v_idModulo = request.GET.get('idModulo')
    if (v_idModulo != ""):
        data_modulo = list(fc_get_module(v_idModulo))
        data_to_array = []
        if (data_modulo != ()):
            for i in data_modulo:
                data_to_array.append({
                    "id_modulo": i[0],
                    "nombre_modulo": i[1],
                    "descripcion_modulo": i[2],
                    "status_modulo": i[3],
                })
            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return redirect("getModulosPage")
    else:
        return redirect("getModulosPage")

def enableModulo(request):
    """
    Si el método de solicitud es GET, obtenga el idModulo de la solicitud, verifique si existe, si
    existe, habilítelo, si no, redirija a getModulosPage.
    
    :param request: El objeto de solicitud es una instancia de HttpRequest. Contiene toda la información
    enviada por el cliente
    :return: una redirección a getModulosPage.
    """
    if request.method == "GET":
        v_idModulo = request.GET.get("idModulo")
        exist = fc_get_module(v_idModulo)
        if (exist != ()):
            fc_enable_modulo(v_idModulo)
            return redirect("getModulosPage")
        else:
            return redirect("getModulosPage")
    else:
        return redirect("getModulosPage")

def disableModulo(request):
    """
    Si el método de solicitud es GET, obtenga el idModulo de la solicitud, verifique si existe, si
    existe, desactívelo, si no existe, redirija a getModulosPage.
    
    :param request: El objeto de solicitud es un objeto HttpRequest. Contiene metadatos sobre la
    solicitud, incluido el método HTTP
    :return: una redirección a getModulosPage.
    """
    if request.method == "GET":
        v_idModulo = request.GET.get("idModulo")
        exist = fc_get_module(v_idModulo)
        if (exist != ()):
            fc_deactivate_modulo(v_idModulo)
            return redirect("getModulosPage")
        else:
            return redirect("getModulosPage")
    else:
        return redirect("getModulosPage")

def deleteModulo(request):
    """
    Si el método de solicitud es GET, obtener el idMódulo de la solicitud, comprobar si existe, si lo hace
    lo elimina, si no lo hace, redirige a la página getModulosPage.
    
    :param request: El objeto request es una instancia de HttpRequest. Contiene toda la información
    sobre la solicitud actual
    :return: una redirección a la página getModulosPage.
    """
    if request.method == "GET":
        v_idModulo = request.GET.get("idModulo")
        exist = fc_get_module(v_idModulo)
        if (exist != ()):
            fc_delete_modulo(v_idModulo)
            return redirect("getModulosPage")
        else:
            return redirect("getModulosPage")
    else:
        return redirect("getModulosPage")