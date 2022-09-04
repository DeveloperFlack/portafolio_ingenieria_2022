from apps.dashboard.views import *

# TODOS LOS USUARIOS
def fc_get_all_usuarios():
    """
    Obtiene una conexión, crea un cursor, ejecuta un procedimiento almacenado, obtiene los resultados, cierra la
    conexión y devuelve los resultados
    :return: A list of tuples.
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_usuarios_all()")
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

# OBTENER UN USUARIO
def fc_get_usuario(rut_usuario):
    """
    Obtiene una conexión con la base de datos, crea un cursor, ejecuta un procedimiento almacenado, obtiene los
    resultados, cierra la conexión y devuelve los resultados
    
    :param rut_usuario: '12345678-9'
    :return: Una lista de tuplas.
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_usuarios_get('%s')" % (rut_usuario))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

# INSERTAR USUARIO
def fc_insert_usuario(rut_usuario, primer_nombre, segundo_nombre, apellido_paterno, apellido_materno, correo, password_usuario, telefono, direccion, status_ususario, id_rol):
    """
    Inserta un nuevo usuario en la base de datos.
    
    :param rut_usuario: varchar(10)
    :param primer_nombre: "Juan"
    :param segundo_nombre: "",
    :param apellido_paterno: "Apellido Paterno"
    :param apellido_materno: "string"
    :param correo: varchar(50)
    :param password_usuario: varchar(100)
    :param telefono: int
    :param direccion: varchar(100)
    :param status_ususario: 1
    :param id_rol: 1
    :return: A string
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_usuarios_insert('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s', %s, %s)" %
                           (rut_usuario, primer_nombre, segundo_nombre, apellido_paterno, apellido_materno, correo, password_usuario, telefono, direccion, status_ususario, id_rol))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"

# ACTUALIZAR USUARIO
def fc_update_usuario(rut_usuario, primer_nombre, segundo_nombre, apellido_paterno, apellido_materno, correo, password_usuario, telefono, direccion, status_ususario, id_rol):
    """
    Fc_update_usuario(rut_usuario, primer_nombre, segundo_nombre, apellido_paterno, apellido_materno,
    correo, password_usuario, telefono, direccion, status_ususario, id_rol)
    
    :param rut_usuario: varchar(10)
    :param primer_nombre: First Name
    :param segundo_nombre: '',
    :param apellido_paterno: varchar(50)
    :param apellido_materno: '',
    :param correo: varchar(50)
    :param password_usuario: varchar(100)
    :param telefono: int
    :param direccion: varchar(100)
    :param status_ususario: 1 or 0
    :param id_rol: int
    :return: A string
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_usuarios_update('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s', %s, %s)" %
                           (rut_usuario, primer_nombre, segundo_nombre, apellido_paterno, apellido_materno, correo, password_usuario, telefono, direccion, status_ususario, id_rol))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"

# Activar / Habilitar Usuario
def fc_enable_usuario(rut_usuario):
    """
    Llama a un procedimiento almacenado que permite a un usuario de la base de datos
    
    :param rut_usuario: varchar(10)
    :return: A string
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_usuarios_enable('%s')" % (rut_usuario))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"

# Desactivar / Deshabilitar Usuario
def fc_deactivate_usuario(rut_usuario):
    """
    Llama a un procedimiento almacenado que desactiva un usuario en la base de datos
    
    :param rut_usuario: varchar(10)
    :return: A string
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_usuarios_deactivate('%s')" % (rut_usuario))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"

# Eliminar un Usuario
def fc_delete_usuario(rut_usuario):
    """
    Toma un argumento para eliminar dentro de la base de datos una fila.
    
    :param rut_usuario: varchar(10)
    :return: A string
    """
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_usuarios_delete('%s')" % (rut_usuario))
            cx.commit()
        cx.close()
        return "Realizado con Éxito"
    except Exception as ex:
        print(ex)
        return "Error en el Proceso"