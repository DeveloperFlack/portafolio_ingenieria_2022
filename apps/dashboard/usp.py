from django.conf import settings 
import pymysql


def get_connection ():
    return pymysql.connect (host=settings.DB_HOST, database=settings.DB_SCHEMA, user=settings.DB_USER, password=settings.DB_PASS)


def fc_user_login (rut_usuario, contrasena_usuario):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_usuarios_login('%s', '%s')" % (rut_usuario, contrasena_usuario))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

def fc_get_permisos_with_modulos (id_rol):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL usp_permisos_get_with_modules(%s)" % (id_rol))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print (ex)

