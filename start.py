import os
import sys
import subprocess
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict

def install_requirement(requirement):
    """
    Si el requisito no está instalado, devuelve True
    
    :param requirement: El nombre del paquete que desea instalar
    :return: Un valor booleano.
    """
    should_install = False
    try:
        pkg_resources.require(requirement)
    except (DistributionNotFound, VersionConflict):
        should_install = True
    return should_install


def install_packages(requirement_list):
    """
    Si el módulo no está instalado, instálelo.
    
    :param requirement_list: Una lista de requisitos para instalar
    """
    try:
        requirements = [
            requirement
            for requirement in requirement_list
            if install_requirement(requirement)
        ]
        if len(requirements) > 0:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *requirements])
        else:
            print("El Módulo ya está instalado.")

    except Exception as e:
        print(e)


def get_requirements():
    # Está leyendo el archivo requirements.txt y agregando cada línea a la matriz require_list.
    requirement_list = []
    txtfile = open('requirements.txt', 'r')

    for x in txtfile:
        requirement_list.append(x)

    # Instalación de los paquetes en el archivo requirements.txt.
    install_packages(requirement_list)

array = {}
INPUT_DB_HOST = ""
def get_host():
    INPUT_DB_HOST = input('Host de Base de Datos: ')
    array['HOST'] = INPUT_DB_HOST
    return INPUT_DB_HOST

INPUT_DB_USER = ""
def get_user():
    while True:
        try:
            x = str(input('¿Ha cambiado el Usuario de Base de Datos? (Y/y o N/n): '))
            if (x.lower() == 'y'):
                INPUT_DB_USER = input('USUARIO de Base de Datos: ')
                array['USER'] = INPUT_DB_USER
                return INPUT_DB_USER
            elif (x.lower() == 'n'):
                INPUT_DB_USER = 'portafolionma'
                array['USER'] = INPUT_DB_USER
                return INPUT_DB_USER
            else:
                print ('Ingrese Y/y o N/n')
        except KeyError:
            print ('Ingrese Y/y o N/n')
            continue


INPUT_DB_PASS = ""
def get_pass():
    while True:
        try:
            x = str(input('¿Ha cambiado la contraseña? (Y/y o N/n): '))
            if (x.lower() == 'y'):
                INPUT_DB_PASS = input('PASSWORD de Base de Datos: ')
                array['PASS'] = INPUT_DB_PASS
                return INPUT_DB_PASS
            elif (x.lower() == 'n'):
                INPUT_DB_PASS = 'duoc'
                array['PASS'] = INPUT_DB_PASS
                return INPUT_DB_PASS
            else:
                print ('Ingrese Y/y o N/n')
        except KeyError:
            print ('Ingrese Y/y o N/n')
            continue


INPUT_DB_SCHEMA = ""
def get_schema():
    while True:
        try:
            x = str(input('¿Ha cambiado el SCHEMA? (Y/y o N/n): '))
            if (x.lower() == 'y'):
                    INPUT_DB_SCHEMA = input('SCHEMA de Base de Datos: ')
                    array['SCHEMA'] = INPUT_DB_SCHEMA
                    return INPUT_DB_SCHEMA
            elif (x.lower() == 'n'):
                INPUT_DB_SCHEMA = 'portafolionma1'
                array['SCHEMA'] = INPUT_DB_SCHEMA
                return INPUT_DB_SCHEMA
            else:
                print ('Ingrese Y/y o N/n')
        except KeyError:
            print ('Ingrese Y/y o N/n')
            continue
# Una variable especial en Python que se evalúa como True si el archivo se ejecuta como el programa
# principal.

def get_bbdd():
    host=get_host()
    user=get_user()
    password=get_pass()
    schema=get_schema()
    
    return (host, user, password, schema)


# Ejecutando el servidor.
if __name__ == "__main__":
    get_requirements()
    os.system('python manage.py runserver')