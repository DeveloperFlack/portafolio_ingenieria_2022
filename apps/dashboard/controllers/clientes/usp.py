from apps.dashboard.views import *

def fc_get_all_clientes():
    """
    Obtiene todos los módulos de la base de datos
    :return: A list of tuples.
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_clientes_all()")
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

def fc_enable_disable_clientes(rut_cliente):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL USP_ENABLE_DISABLE_CLIENTES(%s)" % (rut_cliente))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

def fc_get_cliente_dash(rut_cliente):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_clientes_get('%s')" % (rut_cliente))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

def fc_update_cliente(rut_cliente, contrasena_cliente, correo_cliente, telefono_cliente, nombre_empresa):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_clientes_update('%s', '%s', '%s', '%s', '%s')" % (rut_cliente, contrasena_cliente, correo_cliente, telefono_cliente, nombre_empresa))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)
 

