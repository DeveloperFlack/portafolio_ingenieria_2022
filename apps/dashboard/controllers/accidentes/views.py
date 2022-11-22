from genericpath import exists
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
import pymysql
import hashlib
from apps.dashboard.usp import get_connection
from .views import *
from apps.dashboard.controllers.roles.usp import fc_get_permisos
from django.contrib import messages
from apps.helpers import request_session

def getAccidentesPage(request):
    data = {
        'id' : 8,
        'meta_title': 'Dashboard - Accidentes',
        'breadcrumb': "Accidentes",
        'title': 'Lista de Accidentes',
        'subtitle': 'Lista completa de Accidentes',
        'button_add': 'Añadir Accidentes',
    }
    return render(request, "accidentes.html", data)

def disable_accidente(request):
    if (request.method == 'GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_accidente = request.GET.get('idAccidente')
                cursor.execute("SELECT * FROM nma_accidentes WHERE id_accidente = %s" % (v_id_accidente))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("UPDATE nma_accidentes SET status_accidente = 0 WHERE id_accidente = %s" % (v_id_accidente))
                    cx.commit()
                    messages.add_message(request, messages.SUCCESS, 'Accidente Desactivado exitosamente!')
                    return redirect("getAccidentesPage")
                else:
                    messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
                    return redirect("getAccidentesPage")
        except Exception as ex:
            print(ex)
            return redirect("getAccidentesPage")
    else:
        return redirect("getAccidentesPage")

def enable_accidente(request):
    if (request.method == 'GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_accidente = request.GET.get('idAccidente')
                cursor.execute("SELECT * FROM nma_accidentes WHERE id_accidente = %s" % (v_id_accidente))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("UPDATE nma_accidentes SET status_accidente = 1 WHERE id_accidente = %s" % (v_id_accidente))
                    cx.commit()
                    messages.add_message(request, messages.SUCCESS, 'Accidente Desactivado exitosamente!')
                    return redirect("getAccidentesPage")
                else:
                    messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
                    return redirect("getAccidentesPage")
        except Exception as ex:
            print(ex)
            return redirect("getAccidentesPage")
    else:
        return redirect("getAccidentesPage")

def get_accidentes (request):
    if(request.method=='GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_accidente = request.GET.get("idAccidente")

                cursor.execute("SELECT * FROM nma_accidentes WHERE id_accidente = %s" % (v_id_accidente))
                exist = cursor.fetchall()

                data_to_array = []

                if (exist != ()):
                    for i in exist:
                        data_to_array.append({
                            "id_accidente": i[0],
                            "rut_cliente": i[1],
                            "nombre_accidente": i[2],
                            "descripcion_accidente" : i[3],
                            "fecha_accidente": i[4],
                            "hora_accidente": i[5],
                            "tipo_accidente": i[6],
                        })

            cx.close()
            return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as ex:
            print(ex)
            messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
            return redirect("getAccidentesPage")
    else:
        return redirect("getAccidentesPage")

def delete_accidentes(request):
    if(request.method=='GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                v_id_accidente = request.GET.get("idAccidente")

                cursor.execute("SELECT * FROM nma_accidentes WHERE id_accidente = %s" % (v_id_accidente))
                exist = cursor.fetchall()

                if (exist != ()):
                    cursor.execute("DELETE FROM nma_accidentes WHERE id_accidente = %s" % (v_id_accidente))
                    cx.commit()

            cx.close()
            return redirect("getAccidentesPage")
        except Exception as ex:
            print(ex)
            messages.add_message(request, messages.ERROR, 'Ha ocurrido un error inesperado, vuelva a intentarlo!')
            return redirect("getAccidentesPage")
    else:
        return redirect("getAccidentesPage")

def getAllAccidentes(request):
    if(request.method == 'GET'):
        try:
            cx = get_connection()
            with cx.cursor() as cursor:
                cursor.execute("SELECT * FROM nma_accidentes")
                data_accidentes = cursor.fetchall()
                data_to_array = []
                for i in data_accidentes:
                    data_to_array.append({
                        "id_accidente" : i[0],
                        "rut_cliente": i[1],
                        "nombre_accidente": i[2],
                        "descripcion_accidente": i[3],
                        "fecha_accidente": i[4],
                        "hora_accidente": i[5],
                        "tipo_accidente": i[6],
                        "status_accidente": i[7],
                    })

                for i in data_to_array:
                    if (i['status_accidente'] == 1):
                        i['status_accidente'] = """<div class='text-center'><button class='btn btn-sm btn-success' 
                            style='background: linear-gradient(to right, deepskyblue, blueviolet); border: none;'>Activado</button></div>"""
                    else:
                        i['status_accidente'] = """<div class='text-center'><button class='btn btn-sm btn-danger' 
                            style='background: linear-gradient(to right, orange, deeppink); border: none; color: white;'>Desactivado</button></div>"""

                    i['options'] = """
                        <div class='text-center'>
                            <a onclick='fntEnableAccidente(%s)' class='btn btn-sm btn-success'><i class='bx bx-power-off' ></i></a>
                            <a onclick='fntDisableAccidente(%s)' class='btn btn-sm btn-warning'><i class='bx bx-power-off' ></i></a>
                            <a onclick='fntConfirmDelete(%s)' class='btn btn-sm btn-danger'><i class='bx bxs-trash-alt'></i></a>
                        </div>
                    """ % (i['id_accidente'],i['id_accidente'],i['id_accidente'])

                return JsonResponse(data_to_array, safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as ex:
            print(ex)
            