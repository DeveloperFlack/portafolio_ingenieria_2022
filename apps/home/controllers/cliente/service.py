from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
from apps.home.views import get_connection
import random
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from datetime import datetime
from dateutil import parser

from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction

from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_type import IntegrationType
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.options import WebpayOptions
from transbank.webpay.webpay_plus.transaction import Transaction
tx = Transaction(WebpayOptions("597055555532", "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C", IntegrationType.TEST))

@csrf_exempt 
def payService(request, params):
    try:
        v_id = params['numberCapacitacion']
        if (v_id == ""):
            v_id = 0
        
        cx = get_connection()
        with cx.cursor() as cursor:
            if (v_id != 0):
                buy_order = params['buyOrder']
                session_id = str(random.randrange(1000000, 99999999))
                
                url = request.build_absolute_uri()
                url = url.split('/')
                
                return_url = "http://localhost:8000/cliente/confirm-pay"
                
                cursor.execute(f"""SELECT * FROM nma_capacitacion WHERE id_capacitacion = {v_id} """)
                data_capacitacion = cursor.fetchall()

                cursor.execute(f"""SELECT * FROM nma_asesoria WHERE id_asesoria = {v_id} """)
                data_asesoria = cursor.fetchall()

                if (data_capacitacion != ()):
                    array_cpc = []
                
                    for x in data_capacitacion :
                        array_cpc.append({
                            'id' : x[0],
                            'rut' : x[1],
                            'nombre' : x[2],
                            'descripcion' : x[3],
                            'total' : x[4],
                            'status' : x[5],
                            'fecha' : x[6]
                        })
                        
                    amount = array_cpc[0]['total']
                    response = tx.create(buy_order, session_id, amount, return_url)
                    request.session["cliente"]["transbank"] = {
                        "id_ass" : v_id,
                        "token" : response['token'] }
                    return redirect (response['url']+'?token_ws='+response['token'])
                elif (data_asesoria != ()):
                    array_ass = []
                
                    for x in data_asesoria :
                        array_ass.append({
                            'id' : x[0],
                            'rut' : x[1],
                            'nombre' : x[2],
                            'descripcion' : x[3],
                            'total' : x[4],
                            'status' : x[5]
                        })
                        
                    amount = array_ass[0]['total']
                    response = tx.create(buy_order, session_id, amount, return_url)
                    request.session["cliente"]["transbank"] = {
                            "id_ass" : v_id,
                            "token" : response['token'] 
                        }

                    return redirect (response['url']+'?token_ws='+response['token'])
                else:
                    return redirect('profileCliente') 
            else:
                return redirect('profileCliente') 

    except Exception as ex:
        print (ex)
        return redirect('profileCliente')
        
def afterPayService (request):
    try:
        cx = get_connection()

        with cx.cursor() as cursor:
            # python-dateutil
            # http://localhost:8000/cliente/confirm-pay?token_ws=01ab37b52ce811a58f116537c478e293c761b11b0ad507eb4292f89bff37ce0b
            # http://localhost:8000/cliente/confirm-pay?token_ws=01ab1e2a4bb31d26b746c9fe0bcc0f06b674eb5b284beec69c46ddad40bad767

            status = tx.status(request.GET.get('token_ws'))
            date = parser.parse(status['transaction_date'])
            status['transaction_date'] = date.strftime("%d-%m-%Y %H:%M:%S")
            data = {
                'transbank_status' : status
            }
            
            cursor.execute(f"""SELECT 
                        sc.rut_cliente, 
                        sc.nombre_solicitud,
                        sc.descripcion_solicitud,
                        sc.estado_solicitud,
                        sc.status_solicitud,
                        cap.nombre_capacitacion
                    FROM nma_solicitudes sc JOIN nma_capacitacion cap
                        on (sc.id_capacitacion = cap.id_capacitacion)
                    WHERE 
                        sc.order_id = {status['buy_order']}
                    """)
            field_names = [i[0] for i in cursor.description ]
            result = [dict(zip(field_names, row)) for row in cursor.fetchall()]

            cursor.execute(f"""SELECT 
                        sc.rut_cliente, 
                        sc.nombre_solicitud,
                        sc.descripcion_solicitud,
                        sc.estado_solicitud,
                        ase.total_asesoria,
                        sc.status_solicitud,
                        ase.nombre_asesoria
                    FROM nma_solicitudes sc JOIN nma_asesoria ase
                        on (sc.id_capacitacion = ase.id_asesoria)
                    WHERE 
                        sc.order_id = {status['buy_order']}
                    """)
            
            field_names3 = [i[0] for i in cursor.description ]
            result3 = [dict(zip(field_names3, row)) for row in cursor.fetchall()]
 
            if (result != []):
                data['data_capacitacion'] = result
                data['data_asesoria'] = False

                cursor.execute(f"""UPDATE nma_solicitudes 
                    SET 
                        estado_solicitud = 1 
                    WHERE 
                        order_id = {status['buy_order']}""")
                        
                cx.commit()


            if (result3 != []):
                data['data_capacitacion'] = False
                data['data_asesoria'] = result3
                
                cursor.execute(f"""UPDATE nma_solicitudes 
                    SET 
                        estado_solicitud = 1 
                    WHERE 
                        order_id = {status['buy_order']}""")

                cx.commit()
                

            return render (request, 'confirm-pay.html', data)

    except Exception as ex:
        print (ex)
        return redirect('profileCliente')