from django.conf import settings 
import pymysql

def get_connection ():
    return pymysql.connect (host=settings.DB_HOST, database=settings.DB_SCHEMA, user=settings.DB_USER, password=settings.DB_PASS)

# OBTENER UN USUARIO
def fc_get_profesional(rut_usuario):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("CALL USP_USUARIOS_GET('%s')" % (rut_usuario))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

def fc_usuarios_login (rut_usuario, password_usuario):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_clientes_login('%s', '%s')" % (rut_usuario, password_usuario))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)


    