from apps.dashboard.urls import *

def session_user_exist (request):
    x = 'usuario' in request.session
    return x

""" Entrar al Dashboard """
def session_user_role(request):
    if ((request.session['usuario']['id_rol'] != 1) & 
        (request.session['usuario']['id_rol'] != 4)):
        return True

""" Entrar a Módulos Dashboard """
def request_module(request, data):
    """
    Si el usuario tiene permiso para leer el módulo, devuelve True.
    
    :param request: es el objeto de la solicitud
    :param data: {'id': 1, 'nombre': 'Modulo 1', 'descripcion': 'Modulo 1', 'url': 'modulo1'}
    :return: Verdadero o falso
    """
    for x in request.session['usuario']['permisos']:
        if ((x['id_modulo'] == data['id']) & (x['read'] == 1)):
            return True 
        
def request_session_cliente(request):
    """
    Si la variable de sesión 'cliente' existe, devuelve True, de lo contrario devuelve False.
    
    :param request: El objeto de la solicitud
    :return: Un valor booleano.
    """
    session_status = 'cliente' in request.session
    return session_status

def request_session_profesional (request):
    """
    Si la variable de sesión 'profesional' existe, devuelve True, de lo contrario, devuelve False
    
    :param request: El objeto de la solicitud
    :return: Un valor booleano.
    """
    session_status = 'profesional' in request.session
    return session_status

def request_session (request):
    session_status_profesional = 'profesional' in request.session
    session_status_cliente = 'cliente' in request.session
    
    if (session_status_profesional != False):
        data = {
            'profesional' : True,
            'cliente': False
        }
        return data
    
    if (session_status_cliente != False):
        data = {
            'profesional' : False,
            'cliente' : True
        }
        return data
    
    data = {
        'session' : False,
        'profesional' : False,
        'cliente': False
    }
    return data