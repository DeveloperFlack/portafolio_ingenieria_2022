from apps.dashboard.views import *

# TODAS LAS CAPACITACIONES
def fc_get_all_capacitaciones():
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_capacitaciones_all()")
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

# INSERTAR CAPACITACIÓN
def fc_insert_capacitacion(rut_usuario, nombre_capacitacion, descripcion_capacitacion, total_capacitacion):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_capacitaciones_insert('%s', '%s', '%s', '%s')" %
                           (0, nombre_capacitacion, descripcion_capacitacion, total_capacitacion))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"

# OBTENER UNA CAPACITACIÓN
def fc_get_capacitacion(id_capacitacion):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_capacitaciones_get(%s)" % (id_capacitacion))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

# ACTUALIZAR CAPACITACIÓN
def fc_update_capacitacion(id_capacitacion, nombre_capacitacion, descripcion_capacitacion, total_capacitacion):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_capacitaciones_update('%s', '%s', '%s', %s)" % (id_capacitacion, nombre_capacitacion, descripcion_capacitacion, total_capacitacion))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"

# DELETE CAPACITACION
def fc_delete_capacitacion(id_capacitacion):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_capacitaciones_delete(%s)" % (id_capacitacion))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"