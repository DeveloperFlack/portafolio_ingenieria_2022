from django.conf import settings 
import pymysql


def get_connection ():
    return pymysql.connect (host=settings.DB_HOST, database=settings.DB_SCHEMA, user=settings.DB_USER, password=settings.DB_PASS)

# OBTENER UN USUARIO
def fc_get_cliente(rut_cliente):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_clientes_get('%s')" % (rut_cliente))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

def fc_home_register (rut_cliente, contrasena_cliente, n1_cliente, n2_cliente, ap_cliente, am_cliente, correo_cliente, telefono_cliente, rut_empresa_cliente, nombre_empresa, id_rol, status_cliente):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL USP_CLIENTES_INSERT('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s)" % ( rut_cliente, contrasena_cliente, n1_cliente, n2_cliente, 
                                                                                                                            ap_cliente, am_cliente, correo_cliente, telefono_cliente, 
                                                                                                                            rut_empresa_cliente, nombre_empresa, id_rol, status_cliente))
            cx.commit()
            print (cursor)
        cx.close()
        return "Realizado con éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"

def fc_home_login (rut_cliente, contrasena_cliente):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_clientes_login('%s', '%s')" % (rut_cliente, contrasena_cliente))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

def fc_solicitud_insert (rut_cliente, id_capacitacion, nombre_solicitud, descripcion_solicitud, tipo_solicitud, estado_solicitud, status_solicitud):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL USP_SOLICITUDES_INSERT('%s', %s, '%s', '%s', %s, %s, %s)" % (rut_cliente, id_capacitacion, nombre_solicitud, descripcion_solicitud, tipo_solicitud, estado_solicitud, status_solicitud))
            cx.commit()
            print (cursor)
        cx.close()
        return "Realizado con éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"

def fc_get_solicitudes (rut_cliente):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL USP_SOLICITUDES_GET('%s')" % (rut_cliente))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)