import http.server
import http.client
import socketserver
import json


PORT = 8000
socketserver.TCPServer.allow_reuse_address = True



openfda_url="api.fda.gov"
openfda_event="/drug/label.json"
openfda_drug='&search=active_ingredient:'
openfda_company='&search=openfda.manufacturer_name:'


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def main_web(self):   
        html = '''<html>
            <head>
                <title> OpenFDA Web</title>
            </head>
            <body style = 'background-color: green' align='center' >
                <h1> Bienvenidos a nuestra web de OpenFDA </h1>
                <h2> Lista Medicamentos  </h2>
                <form action = 'listDrugs' method ="get">
                    <input type = 'submit' value = 'Listar medicamentos'>
                        Limit = <input type = 'text' name = 'limit' >
                    </input>
                </form>
                <form action = 'searchDrug' method ="get">
                    <input type = 'submit' value = 'Buscar un medicamento'>
                        Drug = <input type = 'text' name = 'drug'>
                    </input>
                </form>
                <h2> Lista Empresas </h2>
                <form action = 'listCompanies' method ="get">
                    <input type = 'submit' value = 'Listar empresas '>
                        Limit = <input type = 'text' name = 'limit' >
                    </input>
                </form>
                <form action = 'searchCompany' method ="get">
                    <input type = 'submit' value = 'Buscar una empresa'>
                        Company = <input type = 'text' name = 'company'>
                    </input>
                </form>
                <h2> Lista Advertencias </h2>
                <form action = 'listWarnings' method ="get">
                    <input type = 'submit' value = 'Listar Adevertencias'>
                        Limit = <input type = 'text' name = 'limit' >
                    </input>
                </form> Autor: Ruben Burgos Bordel'''
        return html


    def medicamentos_web(self,listar_medicamentos):
        html_farmaco = '''<html>
            <head>
                <title> OpenFDA Medicamentos </title>
            </head>
                <body> mediamentos encontrados:
                    <ul>'''

        for i in listar_medicamentos:
            html_farmaco += '<li>'+i+'</li>'

        html_farmaco += '''</ul>
                    </body>
                    </html>'''

        return html_farmaco


    def empresas_web(self,list_empresas):
        html_empresas = '''<html>
            <head>
                <title> OpenFDA Empresas </title>
            </head>
                <body>  empresas encontradas:
                    <ul>'''

        for i in list_empresas:
            html_empresas += '<li>'+i+'</li>'

        html_empresas += '''</ul>
                    </body>
                    </html>'''

        return html_empresas


    def p_activo_web(self,list_activo):
        html_activo = '''<html>
            <head>
                <title> OpenFDA Principio activo </title>
            </head>'''
        for a in list_activo:
            html_activo +=  '<body> Este principio activo '+ a +' se encuentra en: <ul>'
            break


        for i in list_activo:
            html_activo += '<li>'+i+'</li>'

        html_activo += '''</ul>
                    </body>
                    </html>'''

        return html_activo


    def company_web(self,list_busc_empresa):
        html_busc_empresa = '''<html>
            <head>
                <title> Open FDA Empresa </title>
            </head>'''
        for a in list_busc_empresa:
            html_busc_empresa +=  "<body> La informacion encontrada de la empresa "+ a +' es: <ul>'
            break


        for i in list_busc_empresa:
            html_busc_empresa += '<li>'+i+'</li>'

        html_busc_empresa += '''</ul>
                    </body>
                    </html>'''

        return html_busc_empresa


    def advertencia_web(self,list_advertencia):
        html_advertencia = '''<html>
            <head>
                <title> OpenFDA Warnings </title>
            </head>
                <body>  las adevertencias:
                    <ul>'''

        for i in list_advertencia:
            html_advertencia += '<li>'+i+'</li>'

        html_advertencia += '''</ul>
                    </body>
                    </html>'''

        return html_advertencia


    def error_web(self):
        error = '''<html>
            <head>
                <title> Error </title>
            </head>
            <body>
                <h1> Error found </h1>
                Sin informacion sobre el valor introducido
            </body>
            </html>'''

        return error


    def results(self, limite):
        connection = http.client.HTTPSConnection(openfda_url)
        connection.request("GET", openfda_event + "?limit="+str(limite))
        print(openfda_event + "?limit="+str(limite))
        r1 = connection.getresponse()
        drugs_raw = r1.read().decode("utf8")
        data = json.loads(drugs_raw)
        resultados = data['results']
        return resultados

    def do_GET(self):
        recurso_list = self.path.split("?")
        if len(recurso_list) > 1:
            parametro = recurso_list[1]
        else:
            parametro = ""

        limit = 10

        if parametro:
            parse_limit = parametro.split("=")
            if parse_limit[0] == "limit":
                limit = int(parse_limit[1])
                print("Limit: {}".format(limit))

        else:
            print("Sin parametros")


        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = self.main_web()
            self.wfile.write(bytes(html, "utf8"))

        elif 'listDrugs' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            farmacos = []
            resultados = self.results(limit)
            for resultado in resultados:
                if ('generic_name' in resultado['openfda']):
                    farmacos.append (resultado['openfda']['generic_name'][0])
                else:
                    farmacos.append('Desconocido')

            html_farmaco = self.medicamentos_web(farmacos)
            self.wfile.write(bytes(html_farmaco, "utf8"))

        elif 'listCompanies' in self.path:
            self.send_response(202)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            companias = []
            resultados = self.results(limit)
            for resultado in resultados:
                if ('manufacturer_name' in resultado['openfda']):
                    companias.append (resultado['openfda']['manufacturer_name'][0])
                else:
                    companias.append('Desconocido')

            html_empresas = self.empresas_web(companias)
            self.wfile.write(bytes(html_empresas, "utf8"))


        elif 'searchDrug' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            drug=self.path.split('=')[1]

            conn = http.client.HTTPSConnection(openfda_url)
            conn.request("GET", openfda_event + "?limit="+str(limit)+ openfda_drug + drug)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf8")
            data = json.loads(drugs_raw)

            try:
                resultados = data['results']

                princip_activo = []
                for resultado in resultados:
                    if ('generic_name' in resultado['openfda']):
                        princip_activo.append (resultado['openfda']['generic_name'][0])
                    else:
                        princip_activo.append('Desconocido')

                html_activo = self.p_activo_web(princip_activo)
                self.wfile.write(bytes(html_activo, "utf8"))

            except KeyError:
                error = self.error_web()
                self.wfile.write(bytes(error, "utf8"))

        elif 'listWarnings' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            advertencias = []
            resultados = self.results(limit)
            for resultado in resultados:
                if ('warnings' in resultado):
                    advertencias.append (resultado['warnings'][0])
                else:
                    advertencias.append('Desconocido')

            html_advertencia = self.advertencia_web(advertencias)
            self.wfile.write(bytes(html_advertencia, "utf8"))



        elif 'searchCompany' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            empresa = self.path.split('=')[1]
            connection = http.client.HTTPSConnection(openfda_url)
            connection.request("GET", openfda_event + "?limit="+str(limit)+ openfda_company + empresa)
            r1 = connection.getresponse()
            drugs_raw = r1.read().decode("utf8")
            data = json.loads(drugs_raw)

            try:
                resultados = data['results']

                empresas = []
                for resultado in resultados:
                    empresas.append(resultado['openfda']['manufacturer_name'][0])


                html_busc_empresa = self.company_web(empresas)
                self.wfile.write(bytes(html_busc_empresa, "utf8"))

            except KeyError:
                error = self.error_web()
                self.wfile.write(bytes(error, "utf8"))


        elif 'redirect' in self.path:
            self.send_response(302)
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()

        elif 'secret' in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("No encontramos el recurso '{}'".format(self.path).encode())
        return


Handler = testHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Sirviendo al puerto", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Interrumpido ")

print("")
print("parado")
