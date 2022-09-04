import apps.config as cf
import pymysql


def get_connection ():
    return pymysql.connect (host=cf.DB_HOST, database=cf.DB_SCHEMA, user=cf.DB_USER, password=cf.DB_PASS)


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
