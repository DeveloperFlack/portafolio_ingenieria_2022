from apps.dashboard.views import *

# TODOS LOS ROLES
def fc_get_all_roles():
    """
    Obtiene todos los roles de la base de datos y los devuelve como una lista de tuplas
    :return: Una lista de tuplas.
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL USP_ROLES_ALL()")
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print (ex)

# OBTENER UN ROL
def fc_get_roles (id_modulo):
    """
    Obtiene una conexión a la base de datos, crea un cursor, ejecuta un procedimiento almacenado,
    obtiene los resultados, cierra la conexión y devuelve los resultados.
    
    :param id_modulo: es el id del modulo
    :return: Una lista de tuplas.
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL USP_ROLES_GET({0})" % (id_modulo))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print (ex)

# INSERTAR ROL
def fc_insert_roles (nombre_rol, descripcion_rol):
    """
    Inserta un Rol en base de datos.
    
    :param nombre_rol: El nombre del papel
    :param descripcion_rol: "Esto es una prueba"
    :return: El resultado de la consulta.
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_roles_insert('%s', '%s', %s)" % (nombre_rol, descripcion_rol, 0))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print (ex)
        return "Error en el Proceso"


# ACTUALIZAR ROL
def fc_update_roles(id_rol, nombre_rol, descripcion_rol):
    """
    Toma tres parámetros, llama a un procedimiento almacenado con esos parámetros y actualiza el Rol dentro de base de datos.
    
    :param id_rol: En t
    :param nombre_rol: "Administrador"
    :param descripcion_rol: "Esto es una prueba"
    :return: El resultado de la consulta.
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_roles_udpate(%s, '%s', '%s', %s)" %
                           (id_rol, nombre_rol, descripcion_rol, 0))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"


# Activar / Habilitar Rol
def fc_enable_roles(id_rol):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_roles_enable(%s)" % (id_rol))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"


# Desactivar / Deshabilitar Rol
def fc_deactivate_roles(id_rol):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_roles_deactivate(%s)" % (id_rol))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"


# Eliminar Rol
def fc_delete_roles(id_rol):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_roles_delete(%s)" % (id_rol))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"


def fc_get_enabled_modulos():
    """
    Obtiene una conexión, crea un cursor, ejecuta un procedimiento almacenado, obtiene los resultados,
    cierra la conexión y devuelve los resultados, en dónde llegan datos de módulos activados dentro de 
    base de datos.

    :return: Una lista de tuplas.
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL USP_MODULOS_ENABLED()")
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print (ex)

def fc_get_permisos (id_rol):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL USP_PERMISOS_GET(%s)" % (id_rol))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print (ex)

def fc_insert_permisos(id_modulo, id_rol, c, r, u, d):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_permisos_insert(%s, %s, %s, %s, %s, %s)" % (id_modulo, id_rol, c, r, u, d))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print (ex)
        return "Error en el Proceso"

def fc_delete_permisos(id_rol):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_permisos_delete(%s)" % (id_rol))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print (ex)
        return "Error en el Proceso"