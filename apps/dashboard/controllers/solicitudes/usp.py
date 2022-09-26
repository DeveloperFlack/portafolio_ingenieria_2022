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
            cursor.execute("CALL USP_SOLICITUDES_UPDATE(%s, %s, %s, %s)" % (id_solicitud, fecha, time_start, time_end))
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

# OBTENER UNA SOLICITUD
def fc_get_solicitud_all (id_solicitud):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL USP_SOLICITUDES (%s)" % (id_solicitud))
            result = cursor.fetchall()
            print (result)
        cx.close()
        return result
    except Exception as ex:
        print (ex)