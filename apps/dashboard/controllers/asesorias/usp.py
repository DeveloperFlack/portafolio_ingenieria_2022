from apps.dashboard.views import *

# Todas las Asesorías
def fc_get_all_asesorias():
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_asesoria_all()")
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

#Insertar Asesorias
def fc_insert_asesorias(rut_ususario, nombre_asesoria, descripcion_asesoria, total_asesoria):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_asesoria_insert('%s', '%s', '%s', %s)" % (rut_ususario, nombre_asesoria, descripcion_asesoria, total_asesoria))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"

#Obtener una Asesoria
def fc_get_asesoria(id_asesoria):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_asesoria_get(%s)" % (id_asesoria))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

#Actualizar Asesoria
def fc_update_asesoria(id_asesoria, rut_usuario, nombre_asesoria, descripcion_asesoria, total_asesoria):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_asesoria_update(%s, '%s', '%s', '%s', %s)" % (id_asesoria, rut_usuario, nombre_asesoria, descripcion_asesoria, total_asesoria))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"

#Delete Asesoria
def fc_delete_asesoria(id_asesoria):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_asesoria_delete(%s)" % (id_asesoria))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"