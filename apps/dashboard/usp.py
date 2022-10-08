from django.conf import settings 
import pymysql


def get_connection ():
    return pymysql.connect (host=settings.DB_HOST, database=settings.DB_SCHEMA, user=settings.DB_USER, password=settings.DB_PASS)


def fc_user_login (rut_usuario, password_usuario):
    try:
        cx = get_connection()
        with cx.cursor() as cursor:
            cursor.execute("call usp_usuarios_login('%s', '%s')" % (rut_usuario, password_usuario))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print(ex)

def fc_get_permisos_with_modulos_1(id_rol):
    try:
        cx =  get_connection()
        with cx.cursor() as cursor:
            cursor.execute("SELECT * FROM nma_modulo USS JOIN nma_permisos PER ON (USS.id_modulo = PER.id_modulo) WHERE PER.id_rol = %s" % (id_rol))
            result = cursor.fetchall()
        cx.close()
        return result
    except Exception as ex:
        print (ex)