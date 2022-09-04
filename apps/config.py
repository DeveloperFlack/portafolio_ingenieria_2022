# Configuración del host, el usuario, la contraseña y el esquema de la base de datos.
DB_HOST = 'localhost'
DB_USER = 'portafolionma'
DB_PASS = 'duoc'
DB_SCHEMA = 'portafolionma1'

# Cambiar el nombre de la tabla donde se almacenan las sesiones.
from django.contrib.sessions.models import Session
if (Session._meta.db_table == "django_session"):
    Session._meta.db_table = "nma_sessions"