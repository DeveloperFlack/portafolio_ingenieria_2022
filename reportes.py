import os,django
from django.conf import settings
from weasyprint import HTML, CSS
from apps.dashboard.usp import get_connection

def generarReporte(request):
    if (request.method == 'GET'):
        v_nombre = request.GET.get('')
        v_edad = str(24)

        data_array = []
    
        data_array.append({
            'nombre_cliente': v_nombre,
            'nombre_empresa': v_edad,
        })


        html = HTML(string="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <head>
                <meta charset='utf-8'>
                <meta http-equiv='X-UA-Compatible' content='IE=edge'>
                <title>RSP Company - Asesores Profesionales1</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>
                <div class="container">
                    <div class="content_logo text-center">
                        <img src="https://assets.stickpng.com/thumbs/5847f439cef1014c0b5e4890.png" class="p-3 rounded-circle" style="width: 15%">                    
                        <h1>RSP Company Report</h1>
                        <h1>""" + data_array[0]['nombre_cliente'] + " " + data_array[0]['nombre_empresa'] + """</h1>
                    </div>
                    <div class="info_report">
                        <div class="descripcion_reporte">
                            <p>
                                Lorem ipsum dolor, sit amet consectetur adipisicing elit. Odit, ex dicta quibusdam illo culpa aut ducimus eaque reprehenderit labore fuga nemo ullam deleniti voluptatibus. Architecto voluptate doloremque saepe similique inventore.
                                Cum rerum est libero cupiditate saepe impedit exercitationem quae iste? Eveniet a libero esse architecto ipsa repudiandae nulla sunt adipisci mollitia perspiciatis delectus hic enim fugit magni, modi, dicta at?
                                Minima corporis maxime dicta, natus aliquam omnis ipsa, cum veniam, velit molestiae quibusdam neque aperiam nulla exercitationem fugit. Eos molestiae odit debitis itaque eum excepturi veritatis alias possimus at corporis!
                            </p>
                        </div>
                        <table class="table">
                            <thead>
                                <th>Cliente</th>
                                <th>Empresa</th>
                                <th>Rut Empresa</th>
                            </thead>
                            <thead>
                                <th>Juan Palma</th>
                                <th>DUOC UC</th>
                                <th>78875443-2</th>
                            </thead>
                        </table>
                    </div>
                </div>       

            </body>
        </body>
        </html>
        """)

        html.write_pdf('salida.pdf')

    generarReporte()



