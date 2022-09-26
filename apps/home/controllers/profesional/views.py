from genericpath import exists
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .usp import *
import pymysql
import hashlib
from apps.dashboard.controllers.roles.usp import fc_get_permisos
from apps.dashboard.controllers.usuarios.usp import *
from django.contrib import messages
from apps.helpers import request_session_profesional

# Create your views here.

def profileProfesional(request):
    status = request_session_profesional(request)
    if (status == False):
        return redirect('getHome')
    
    #data = {
        #'table' : getSolicitudes(request)
    #}
    
    return render(request, 'profile-professional.html')