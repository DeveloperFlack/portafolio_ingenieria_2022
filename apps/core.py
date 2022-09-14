# Cambiar el nombre de la tabla donde se almacenan las sesiones.
from django.contrib.sessions.models import Session
if (Session._meta.db_table == "django_session"):
    Session._meta.db_table = "nma_sessions"
