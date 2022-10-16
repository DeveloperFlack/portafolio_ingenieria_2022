from random import randint
from apps.dashboard.urls import getDashboard
import pytest
from apps.dashboard.controllers.clientes.usp import *

random_int = randint(111111111111,999999999999)
rut_aleatorio = str(random_int)
Test = 'Test'
TestEdit= 'TestEdit'


def test_registro_cliente():
        rut_cliente = rut_aleatorio
        v_contrasena_cliente = Test
        v_n1_cliente = Test
        v_n2_cliente = Test
        v_ap_cliente = Test
        v_am_cliente = Test
        v_correo_cliente = Test
        v_telefono_cliente = 123456789
        v_rut_empresa_cliente = rut_aleatorio
        v_nombre_empresa = 1
        v_status_cliente = 1
        
        fc_insert_cliente(rut_cliente, v_contrasena_cliente, v_n1_cliente, v_n2_cliente,
                v_ap_cliente, v_am_cliente, v_correo_cliente, v_telefono_cliente, v_rut_empresa_cliente, v_nombre_empresa, v_status_cliente)
        
        consulta= list(fc_get_cliente_dash(rut_aleatorio))
        data_to_array= []
        
        for i in consulta:
                data_to_array.append({
                        'rut_cliente':i[0]
                })  
        assert(data_to_array[0]['rut_cliente'] == rut_aleatorio)

def test_update_cliente():
        rut_cliente = rut_aleatorio
        v_contrasena_cliente = TestEdit
        v_correo_cliente = TestEdit
        v_telefono_cliente = 123456789
        v_nombre_empresa = 1    

        fc_update_cliente(rut_cliente, v_contrasena_cliente, v_correo_cliente, v_telefono_cliente, v_nombre_empresa)

        consulta= list(fc_get_cliente_dash(rut_aleatorio))
        data_to_array= []
        
        for i in consulta:
                data_to_array.append({
                        'rut_cliente':i[0]
                })  
        assert(data_to_array[0]['rut_cliente'] == rut_aleatorio)

def test_eliminar_cliente():
        resultado=fc_delete_cliente(rut_aleatorio)

        assert(resultado == 'Realizado con Éxito')