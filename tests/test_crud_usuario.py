from random import randint
from apps.dashboard.urls import getDashboard
import pytest
from apps.dashboard.controllers.usuarios.usp import fc_delete_usuario, fc_get_usuario, fc_insert_usuario, fc_update_usuario

random_int = randint(111111111111,999999999999)
rut_aleatorio = str(random_int)
Test = 'Test'
TestEdit= 'TestEdit'

## Inicio del test, crea un nuevo usuario con un rut aleatorio, posteriormente verifica si el 
## usuario realmente se insertó en la base de datos
def test_registro_usuario():
        v_rut_usuario = rut_aleatorio
        v_primer_nombre = Test
        v_segundo_nombre = Test
        v_apellido_paterno = Test
        v_apellido_materno = Test
        v_correo = Test
        v_password = Test
        v_telefono = '123456789'
        v_direccion = 'Av. Test 1234'
        v_status_usuario = 1
        v_id_rol = 2
        
        fc_insert_usuario(v_rut_usuario, v_primer_nombre, v_segundo_nombre, v_apellido_paterno,
                v_apellido_materno, v_correo, v_password, v_telefono, v_direccion, v_status_usuario, v_id_rol)
        
        consulta= list(fc_get_usuario(rut_aleatorio))
        data_to_array= []
        
        for i in consulta:
                data_to_array.append({
                        'rut_usuario':i[0]
                })  
        assert(data_to_array[0]['rut_usuario'] == rut_aleatorio)
        
def test_editar_usuario():
        v_rut_usuario = rut_aleatorio
        v_primer_nombre = TestEdit
        v_segundo_nombre = TestEdit
        v_apellido_paterno = TestEdit
        v_apellido_materno = TestEdit
        v_correo = TestEdit
        v_password = TestEdit
        v_telefono = '123456789'
        v_direccion = 'Av. Test 1234'
        v_status_usuario = 1
        v_id_rol = 2        

        fc_update_usuario(v_rut_usuario, v_primer_nombre, v_segundo_nombre, v_apellido_paterno,
                v_apellido_materno, v_correo, v_password, v_telefono, v_direccion, v_status_usuario, v_id_rol)

        consulta= list(fc_get_usuario(rut_aleatorio))
        data_to_array= []
        
        for i in consulta:
                data_to_array.append({
                        'primer_nombre':i[1]
                })  
        assert(data_to_array[0]['primer_nombre'] == TestEdit)

def test_eliminar_usuario():
        resultado=fc_delete_usuario(rut_aleatorio)

        assert(resultado == 'Realizado con Éxito')