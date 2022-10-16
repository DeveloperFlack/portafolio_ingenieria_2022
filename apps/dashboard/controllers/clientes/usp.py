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
            cursor.execute("CALL usp_clientes_update('%s', '%s', '%s', %s, '%s')" % (rut_cliente, contrasena_cliente, correo_cliente, telefono_cliente, nombre_empresa))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)
 
# Insertar cliente
def fc_insert_cliente(rut_cliente, v_contrasena_cliente, v_n1_cliente, v_n2_cliente, v_ap_cliente, v_am_cliente, v_correo_cliente, v_telefono_cliente, v_rut_empresa_cliente, v_nombre_empresa,v_status_cliente):
    """
    Inserta un nuevo cliente en la base de datos.
    
    :param rut_cliente: varchar(10)
    :param v_contrasena_cliente: "Password"
    :param v_n1_cliente: "Juan",
    :param v_n2_cliente: "Ignacio"
    :param v_ap_cliente: "Apellido Paterno"
    :param v_am_cliente: "Apellido Paterno"
    :param v_correo_cliente: varchar(50)
    :param v_telefono_cliente: int
    :param v_rut_empresa_cliente: varchar(12)
    :param v_nombre_empresa: varchar(75)
    :param v_id_rol: 1
    :param v_status_cliente: 1
    :return: A string
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_clientes_insert('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s', '%s', %s, %s)" %
                           (rut_cliente, v_contrasena_cliente, v_n1_cliente, v_n2_cliente, v_ap_cliente, v_am_cliente, v_correo_cliente, v_telefono_cliente, v_rut_empresa_cliente, v_nombre_empresa, 2,v_status_cliente))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"

# Eliminar un Cliente
def fc_delete_cliente(rut_cliente):
    """
    Toma un argumento para eliminar dentro de la base de datos una fila.
    
    :param rut_cliente: varchar(12)
    :return: A string
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_clientes_delete('%s')" % (rut_cliente))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"
