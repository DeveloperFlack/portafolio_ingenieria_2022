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

