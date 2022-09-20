from django.conf import settings 
import pymysql


def get_connection ():
    return pymysql.connect (host=settings.DB_HOST, database=settings.DB_SCHEMA, user=settings.DB_USER, password=settings.DB_PASS)

def fc_home_register (rut_usuario, primer_nombre, segundo_nombre, apellido_paterno, apellido_materno, correo, password_usuario, telefono, direccion, status_usuario, id_rol):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_usuarios_insert('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (rut_usuario, primer_nombre, segundo_nombre, apellido_paterno, apellido_materno, correo, password_usuario, telefono, direccion, status_usuario, id_rol))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

def fc_home_login (rut_usuario, contrasena_usuario):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_usuarios_login('%s', '%s')" % (rut_usuario, contrasena_usuario))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)