from django.shortcuts import render, redirect
from django.http import JsonResponse
from .usp import *
from apps.dashboard.views import multiform
import apps.helpers as helpers

def getRolesPage(request):
    data = {
        'id' : 3,
        'meta_title': 'Dashboard - Roles',
        'breadcrumb': "Roles",
        'title': 'Lista de Roles',
        'subtitle': 'Lista completa de roles de Usuario o Profesional',
        'button_add': 'Añadir nuevo rol',
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
        return render(request, "roles.html", data)


"""
Si el método de solicitud es POST, compruebe si el idRol está vacío. Si es así, inserte los datos en
la base de datos. Si no es así, actualice los datos en la base de datos.

:param request: El objeto de solicitud es una instancia de HttpRequest. Contiene toda la información
sobre la solicitud enviada por el usuario
:return: una redirección a getRolesPage.
"""
def insertRol(request):
    if request.method == "POST":
        v_idRol = request.POST.get("idRol")
        if (v_idRol == ""):
            # INSERTAR Roles
            v_nombre_roles = request.POST.get("txtNombreRol")
            v_descripcion_roles = request.POST.get("txtDescripcionRol")
            fc_insert_roles(v_nombre_roles, v_descripcion_roles)
            return redirect("getRolesPage")

        else:
            # ACTUALIZAR Roles
            exist = fc_get_roles(v_idRol)
            if (exist != ()):
                v_nombre_roles = request.POST.get("txtNombreRol")
                v_descripcion_roles = request.POST.get("txtDescripcionRol")
                fc_update_roles(v_nombre_roles, v_descripcion_roles)
                return redirect("getRolesPage")
            else:
                return redirect("getRolesPage")

    else:
        return redirect("getRolesPage")


def getAllRoles(request):
    data_modulos = list(fc_get_all_roles())
    data_to_array = []
    # Convertir TUPLA a Array Modificable
    for i in data_modulos:
        data_to_array.append({
            "id_rol": i[0],
            "nombre_rol": i[1],
            "descripcion_rol": i[2],
            "status_rol": i[3],
        })

    # Añadir HTML
    for i in data_to_array:
        if (i['status_rol'] == 1):
            i['status_rol'] = """<div class='text-center'><button class='btn btn-sm btn-success' 
                style='background: linear-gradient(to right, deepskyblue, blueviolet); border: none;'>Activado</button></div>"""
        else:
            i['status_rol'] = """<div class='text-center'><button class='btn btn-sm btn-danger' 
                style='background: linear-gradient(to right, orange, deeppink); border: none; color: white;'>Desactivado</button></div>"""

        i['options'] = """
            <div class='text-center'>
                <button type='button' onclick='fntRolesPermisos(%s)' class='btn btn-sm btn-warning'><i class='bx bxs-key'></i></button>
                <button type='button' class='btn btn-sm btn-primary' onclick='fntEditRol(%s)' 
                    data-bs-toggle='modal' data-bs-target='#modalRoles' style='background: linear-gradient(to right, deepskyblue, blueviolet);
                    border: none;'>
                    <i class='bx bxs-edit' ></i>
                </button>
                <a onclick='enableRol(%s)' class='btn btn-sm btn-success'><i class='bx bx-power-off' ></i></a>
                <a onclick='disableRol("%s")' class='btn btn-sm btn-warning'><i class='bx bx-power-off' ></i></a>
                <a onclick='fntConfirmDelete("%s")' class='btn btn-sm btn-danger'><i class='bx bxs-trash-alt'></i></a>
            </div>
        """ % (i['id_rol'], i['id_rol'], i['id_rol'], i['id_rol'], i['id_rol'])

    return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})


def getRol(request):
    v_idMRol = request.GET.get('idRol')
    if (v_idMRol != ""):
        data_rol = fc_get_roles(v_idMRol)
        data_to_array = []
        if (data_rol != ()):
            for i in data_rol:
                data_to_array.append({
                    "id_rol": i[0],
                    "nombre_rol": i[1],
                    "descripcion_rol": i[2],
                    "status_rol": i[3],
                })
            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return redirect("getRolesPage")
    else:
        return redirect("getRolesPage")


"""
Si el método de solicitud es GET, obtenga el idRol de la solicitud, verifique si existe, si existe,
luego habilite el rol y redirija a getRolesPage

:param request: El objeto de solicitud es una instancia de HttpRequest. Contiene toda la información
enviada por el cliente
:return: una redirección a getRolesPage.
"""

def enableRol(request):
    if request.method == "GET":
        v_idRol = request.GET.get("idRol")
        exist = fc_get_roles(v_idRol)
        if (exist != ()):
            fc_enable_roles(v_idRol)
            return redirect("getRolesPage")
        else:
            return redirect("getRolesPage")
    else:
        return redirect("getRolesPage")


"""
    Si el método de solicitud es GET, obtenga el idRol de la solicitud, verifique si existe, si existe,
    desactívelo, si no existe, redirija a getRolesPage
    
    :param request: El objeto de solicitud es una instancia de HttpRequest. Contiene toda la información
    sobre la solicitud actual
    :return: una redirección a getRolesPage.
    """
def disableRol(request):
    if request.method == "GET":
        v_idRol = request.GET.get("idRol")
        exist = fc_get_roles(v_idRol)
        if (exist != ()):
            fc_deactivate_roles(v_idRol)
            return redirect("getRolesPage")
        else:
            return redirect("getRolesPage")
    else:
        return redirect("getRolesPage")

"""
Si el método de solicitud es GET, obtenga el idRol de la solicitud, verifique si existe, si existe,
elimínelo, si no existe, redirija a getRolesPage.

:param request: El objeto de solicitud es una instancia de HttpRequest. Contiene toda la información
sobre la solicitud actual
:return: una redirección a getRolesPage.
"""
def deleteRol(request):
    if request.method == "GET":
        v_idRol = request.GET.get("idRol")
        exist = fc_get_roles(v_idRol)
        if (exist != ()):
            fc_delete_roles(v_idRol)
            return redirect("getRolesPage")
        else:
            return redirect("getRolesPage")
    else:
        return redirect("getRolesPage")


def getPermisos(request):
    if request.method == "GET":
        v_id_rol = request.GET.get("idRol")
        exist = fc_get_roles(v_id_rol)
        if (exist != ()):

            # Obtener los módulos habilitados y colocarlos en una matriz.
            d_a = fc_get_enables_modulos_1()
            data_modulos_array = []

            # Iterando a través de la lista de tuplas y agregando los valores a una lista de
            # diccionarios.
            for x in range(len(d_a)):
                data_modulos_array.append({
                    "id_modulo": d_a[x][0],
                    "nombre_modulo": d_a[x][1],
                    "status_modulo": d_a[x][2]
                })

            # Obtener los permisos para el rol.
            d_b = fc_get_permisos(v_id_rol)
            data_permisos_array = []

            # Iterando a través de la lista de tuplas y agregando los valores a una lista de
            # diccionarios.
            """
            for x in d_b:
                data_permisos_array.append({
                    "id_permiso": x[0],
                    "id_modulo": x[1],
                    "id_rol": x[2],
                    "c": x[3],
                    "r": x[4],
                    "u": x[5],
                    "d": x[6],
                })
            """
            for x in range(len(d_b)):
                data_permisos_array.append({
                    "id_permiso": d_b[x][0],
                    "id_modulo": d_b[x][1],
                    "id_rol": d_b[x][2],
                    "c": d_b[x][3],
                    "r": d_b[x][4],
                    "u": d_b[x][5],
                    "d": d_b[x][6],
                })

            d_c = {'id_rol':  v_id_rol, 'c': 0, 'r': 0, 'u': 0, 'd': 0}
            d_d = {'id_rol': v_id_rol}

            if (d_b == ()):
                for x in range(len(data_modulos_array)):
                    data_modulos_array[x]["permisos"] = d_c
            else:
                for x in range(len(data_modulos_array)):
                    d_c = {
                        'id_rol': v_id_rol,
                        'c': data_permisos_array[x]['c'], 
                        'r': data_permisos_array[x]['r'],
                        'u': data_permisos_array[x]['u'],
                        'd': data_permisos_array[x]['d']
                    }
                    data_modulos_array[x]["permisos"] = d_c

            d_d['RolesModulos'] = data_modulos_array

            d_d['table'] = """ 
                <table class="table">
                    <thead>
                        <th style='color: var(--white-color);'>#</th>
                        <th style='color: var(--white-color);'>Módulos</th>
                        <th style='color: var(--white-color);'>Ver</th>
                        <th style='color: var(--white-color);'>Crear</th>
                        <th style='color: var(--white-color);'>Actualizar</th>
                        <th style='color: var(--white-color);'>Eliminar</th>
                        </thead>
                    <tbody>
                    <tr>
                        <input class="RoleModule_id_role" name="RoleModule_id_role" type="hidden" id="RoleModule_id_role" value="%s" required>
                    </tr>
            """ % (v_id_rol)

            for x in range(len(data_modulos_array)):
                v_id_rol = data_modulos_array[x]["permisos"]['id_rol']
                # Create
                if (data_modulos_array[x]['permisos']['c'] == 1):
                    v_c = " checked "
                else:
                    v_c = ""
                # Read
                if (data_modulos_array[x]['permisos']['r'] == 1):
                    v_r = " checked "
                else:
                    v_r = ""
                # Update
                if (data_modulos_array[x]['permisos']['u'] == 1):
                    v_u = " checked "
                else:
                    v_u = ""
                # Delete
                if (data_modulos_array[x]['permisos']['d'] == 1):
                    v_d = " checked "
                else:
                    v_d = ""

                v_id_module = data_modulos_array[x]['id_modulo']
                v_name_module = data_modulos_array[x]['nombre_modulo']

                d_d['table'] += """ 
                    <tr>
                        <td style='color: var(--white-color);'>%s<input type="hidden" name="m[%s][id_module]" value='%s' required></td>
                        <td style='color: var(--white-color);'>%s</td>
                        <td>
                            <div class='toggle-flip'>
                                <label>
                                    <input type='checkbox' name='m[%s][r]' %s><span class='flip-indecator' data-toggle-on='ON' data-toggle-off='OFF'></span>
                                </label>
                            </div>
                        </td>
                        <td>
                            <div class='toggle-flip'>
                                <label>
                                    <input type='checkbox' name='m[%s][c]' %s><span class='flip-indecator' data-toggle-on='ON' data-toggle-off='OFF'></span>
                                </label>
                            </div>
                        </td>
                        <td>
                            <div class='toggle-flip'>
                                <label>
                                    <input type='checkbox' name='m[%s][u]' %s><span class='flip-indecator' data-toggle-on='ON' data-toggle-off='OFF'></span>
                                </label>
                            </div>
                        </td>
                        <td>
                            <div class='toggle-flip'>
                                <label>
                                    <input type='checkbox' name='m[%s][d]' %s><span class='flip-indecator' data-toggle-on='ON' data-toggle-off='OFF'></span>
                                </label>
                            </div>
                        </td>
                    </tr>
                """ % (x, v_id_module, v_id_module, v_name_module, v_id_module, v_r, v_id_module, v_c, v_id_module, v_u, v_id_module, v_d)
            d_d['table'] += """</body></table> """

            data = {
                'table': d_d['table']
            }
            return render(request, "includes/permisos.html", data)
        else:
            return redirect("getRolesPage")
    else:
        return redirect("getRolesPage")


"""
Si el método de solicitud es POST, obtenga el valor del campo RoleModule_id_role de la solicitud y,
si existe, elimínelo, luego obtenga los valores del campo m de la solicitud y, si existe, insértelo.

:param request: El objeto de la solicitud
:return: <code>&lt;QueryDict: {'csrfmiddlewaretoken': ''}
"""
def setPermisos(request):
    if (request.method == "POST"):
        v_id_role = int(request.POST.get('RoleModule_id_role'))

        exist = fc_get_permisos(v_id_role)
        if (exist != ()):
            fc_delete_permisos(v_id_role)

        a = multiform(request.POST)
        for x in (a['m']):
            c = "c" in a['m'][x]
            r = "r" in a['m'][x]
            u = "u" in a['m'][x]
            d = "d" in a['m'][x]
            # Create
            if (c == False):
                a['m'][x]['c'] = 0
            elif (c == True):
                a['m'][x]['c'] = 1
            
            # Read
            if (r == False):
                a['m'][x]['r'] = 0
            elif (r == True):
                a['m'][x]['r'] = 1
                
            # UPDATE
            if (u == False):
                a['m'][x]['u'] = 0
            elif (u == True):
                a['m'][x]['u'] = 1
            # DELETE
            if (d == False):
                a['m'][x]['d'] = 0
            elif (d == True):
                a['m'][x]['d'] = 1

        for g in (a['m']):
            fc_insert_permisos(
                a['m'][g]['id_module'],
                v_id_role,
                a['m'][g]['c'],
                a['m'][g]['r'],
                a['m'][g]['u'],
                a['m'][g]['d'],
            )

        return redirect('getRolesPage')
    else:
        return redirect('getRolesPage')
