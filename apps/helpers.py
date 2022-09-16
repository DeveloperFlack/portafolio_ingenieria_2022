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
    for x in request.session['usuario']['permisos']:
        if ((x['id_modulo'] == data['id']) & (x['read'] == 1)):
            return True 