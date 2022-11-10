from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
from apps.home.views import get_connection
import random
from django.views.decorators.csrf import csrf_protect, csrf_exempt


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
        v_id_capacitacion = params['numberCapacitacion']
        print (v_id_capacitacion)
        if (v_id_capacitacion == ""):
            v_id_capacitacion = 0
            
        cx = get_connection()
        with cx.cursor() as cursor:
            if (v_id_capacitacion != 0):
                buy_order = str(random.randrange(100, 99999))
                session_id = str(random.randrange(1000000, 99999999))
                
                url = request.build_absolute_uri()
                url = url.split('/')
                return_url_a = redirect('afterPayService')
                # return_url = url[0] + '//' + url[2] + return_url_a.url
                
                return_url = "http://localhost:8000/cliente/confirm-pay"
                
                print (return_url)
                cursor.execute(f"""SELECT * FROM nma_capacitacion WHERE id_capacitacion = '{v_id_capacitacion}' """)
                data_capacitacion = cursor.fetchall()
                array_cpc = []
            
                for x in data_capacitacion :
                    array_cpc.append({
                        'id' : x[0],
                        'rut' : x[1],
                        'nombre' : x[2],
                        'descripcion' : x[3],
                        'total' : x[4],
                        'status' : x[5],
                    })
                    
                amount = array_cpc[0]['total']
                
                response = tx.create(buy_order, session_id, amount, return_url)
                return redirect (response['url']+'?token_ws='+response['token'])
            else:
                return redirect('profileCliente') 

    except Exception as ex:
        print (ex)
        return redirect('profileCliente')
        
def afterPayService (request):
    return render (request, 'confirm-pay.html')


    """ json_nya = request.POST.get('pasaoapoto')
    s1 = json.dumps(json_nya) """