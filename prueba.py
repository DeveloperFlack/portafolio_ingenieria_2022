import pymysql
""" 
    https://newserv.freewha.com/cgi-bin/create_ini.cgi

    diribe6028@lurenwu.com

"""


DB_HOST = 'www.db4free.net'
DB_USER = 'portafolionma1'
DB_PASS = 'portafolionma1'
DB_SCHEMA = 'portafolionma1'

def get_connection():
    return pymysql.connect (host=DB_HOST, database=DB_SCHEMA, user=DB_USER, password=DB_PASS)


""" get_connection() """
try:
    cx = get_connection()
    with cx.cursor as cursor:
        cursor.execute("SELECT * FROM a")
        result = cursor.fetchall()
    cx.close()
    print (result)
except Exception as ex:
    print (ex)
