from apps.dashboard.views import *

# OBTENER SOLICITUDES
def fc_get_all_solicitudes():
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL USP_SOLICITUDES_ALL()")
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

# ACTUALIZAR SOLICITUD
def fc_update_solicitud(id_solicitud, fecha, time_start, time_end):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_solicitudes_update(%s, '%s', '%s', '%s')" % (id_solicitud, fecha, time_start, time_end))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"

# DELETE SOLICITUD
def fc_delete_solicitud(id_solicitud):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL USP_SOLICITUDES_DELETE(%s)" % (id_solicitud))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"

# OBTENER TODAS LAS SOLICITUDES DASHBOARD
def fc_get_solicitud_all ():
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL USP_SOLICITUDES_ALL()")
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print (ex)

# OBTENER UNA SOLICITUD DASHBOARD
def fc_get_solicitudes_dash (id_solicitud):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_solicitudes_get_dash (%s)" % (id_solicitud))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

# ACTIVAR SOLICITUD
def fc_enable_solicitud(id_solicitud):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_solicitudes_enable(%s)" % (id_solicitud))
    except Exception as ex:
        print(ex)

# DESACTIVAR SOLICITUD
def fc_disable_solicitud(id_solicitud):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_solicitudes_disable(%s)" % (id_solicitud))
    except Exception as ex:
        print(ex)