from apps.dashboard.views import *

# TODOS LOS MODULOS
def fc_get_all_modules():
    """
    Obtiene todos los módulos de la base de datos
    :return: A list of tuples.
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL USP_MODULOS_ALL()")
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)


# OBTENER UN MODULO
def fc_get_module(id_modulo):
    """
    Obtiene una conexión con la base de datos, crea un cursor, ejecuta un procedimiento almacenado, obtiene los
    resultados, cierra la conexión y devuelve los resultados
    
    :param id_modulo: int
    :return: A list of tuples.
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_modulos_get(%s)" % (id_modulo))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)


# INSERTAR MODULO
def fc_insert_module(nombre_modulo, descripcion_modulo):
    """
    Toma dos cadenas como parámetros y llama a un procedimiento almacenado que inserta una fila en una tabla
    
    :param nombre_modulo: The name of the module
    :param descripcion_modulo: "This is a test"
    :return: The result of the query.
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_modulos_insert('%s', '%s', %s)" %
                           (nombre_modulo, descripcion_modulo, 0))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"


# ACTUALIZAR MODULO
def fc_update_module(id_modulo, nombre_modulo, descripcion_modulo):
    """
    Toma tres parámetros y llama a un procedimiento almacenado para generar una actualización del módulo con esos parámetros
    
    :param id_modulo: int
    :param nombre_modulo: "Modulo de Prueba"
    :param descripcion_modulo: "This is a test"
    :return: The result of the query.
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_modulos_update(%s, '%s', '%s', %s)" %
                           (id_modulo, nombre_modulo, descripcion_modulo, 0))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"


# Activar / Habilitar Módulo
def fc_enable_modulo(id_modulo):
    """
    Llama a un procedimiento almacenado que habilita un módulo en una base de datos
    
    :param id_modulo: En t
    :return: Una cuerda
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_modulos_enable(%s)" % (id_modulo))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"


# Desactivar / Deshabilitar Módulo
def fc_deactivate_modulo(id_modulo):
    """
    Llama a un procedimiento almacenado que desactiva un módulo en la base de datos.
    
    :param id_modulo: En t
    :return: Una cuerda
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_modulos_deactivate(%s)" % (id_modulo))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"

# Eliminar un Módulo
def fc_delete_modulo(id_modulo):
    """
    Toma un número entero como argumento y luego llama a un procedimiento almacenado que elimina una
    fila de una tabla
    
    :param id_modulo: En t
    :return: Una cuerda
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_modulos_delete(%s)" % (id_modulo))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"
