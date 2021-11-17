from zeroconf import IPVersion, ServiceBrowser, Zeroconf, ZeroconfServiceTypes
import time
import datetime

import json
import requests

#Método para enviar peticiones al servidor web

def enviar(j,peticion):
    jsonToSend={"Peticion":peticion, "info":j}
    jsonToSend=json.dumps(jsonToSend)
    #url="https://exploracion-iot.000webhostapp.com/controlador.php"
    url="http://localhost/ExploracionIoT/controlador.php"
    return requests.post(url, data=jsonToSend)

#Método para obtener vulnerabilidades del servicio
def consultarVulnerabilidades(tipoServicio, nombreServicio):
    url="https://services.nvd.nist.gov/rest/json/cves/1.0/"
    tipoServicioReducido=tipoServicio.split("_")[1].split("_")[0].split(".")[0].replace("-"," ")
    tipoServicioReducido=tipoServicioReducido.upper()
    
    print(tipoServicioReducido)

    if(len(tipoServicioReducido)>=3 and tipoServicioReducido!='HTTP'):
        #Selecciono las vulnerabilidades encontradas en los últimos 3 meses en los servicios:
        fecha=datetime.datetime.now()
        fechaAhora=fecha.strftime("%Y-%m-%dT%H:%M:%S:000 UTC-00:00")
        fechaHace120dias=fecha-datetime.timedelta(days=120)
        fechaHace120dias=fechaHace120dias.strftime("%Y-%m-%dT%H:%M:%S:000 UTC-00:00")
        
        jsonVulnerabil={"keyword":tipoServicioReducido, "resultsPerPage":40,"pubStartDate": fechaHace120dias,
        "pubEndDate":fechaAhora}
        
        r=requests.get(url,params=jsonVulnerabil)
        jsonVul=r.json()
        #este if es para sí con la anterior búsqueda no ha encontrado vulnerabilidades
        if(jsonVul["totalResults"]==0):
            print("Hay que generalizar las vulnerabilidades")
            jsonVulnerabil={"keyword":tipoServicioReducido, "resultsPerPage":10}
            r=requests.get(url,params=jsonVulnerabil)
            return r.json()
        else:
            return r.json()
    else:
        #este else es para si no puede encontrar vulnerabilidades. En este caso, se crea un result vacío
        print("No ha sido posible encontrar vulnerabilidades")
        fecha=datetime.datetime.now()
        fechaAhora=fecha.strftime("%Y-%m-%dT%H:%M:%SZ")
        return  {"resultsPerPage": 0, "startIndex": 0, "totalResults": 0, "result": {}};

#En esta clase se manejan los eventos del serviceBrowser
class MyListener:
    def remove_service(self, zeroconf, type, name):
        print("Service %s removed\n" % (name))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            arrayServicios.append(info)
    def update_service():
        print("Service Updated")

arrayServicios=[]
zeroconf = Zeroconf(ip_version = IPVersion.V4Only)
listener = MyListener()
print("browser")
#El ServiceBrowser crea un hilo, el cual está 3 segundos buscando servicios, hasta que el hilo principal cierre el ServiceBrowser
#el hilo principal detiene este hilo.
print("lista servicios encontrados:")
print(list(ZeroconfServiceTypes.find(zc=zeroconf)))
browser = ServiceBrowser(zeroconf,list(ZeroconfServiceTypes.find(zc=zeroconf)),listener)
time.sleep(3)
browser.cancel()
print(arrayServicios)
#se ordenan los servicios por IPs en un diccionario
serviciosPorIPs={}
mDNSDict={"mDNS":serviciosPorIPs}
for servicio in arrayServicios:
    anyadido=False
    properties={}
    servicio.properties
    for a in servicio.properties:
        clave=str(a)
        clave=clave[2:len(clave)-1]
        valor=str(servicio.properties[a])
        valor=valor[2:len(valor)-1]
        properties[clave]=valor
    for ips in serviciosPorIPs:
        if ips==servicio.parsed_addresses()[0]:
            anyadido=True
            
            serv={"type":servicio.type,"port":servicio.port,
            "weight":servicio.weight,"priority":servicio.priority,"server":servicio.server,"properties":properties,
            "interface_index":servicio.interface_index,"vulnerabilities":consultarVulnerabilidades(servicio.type, servicio.name)}
            ipsPort=str(ips)+":"+str(servicio.port)
            serviciosPorIPs[ipsPort][str(servicio.name)]=serv
        break
    if not anyadido:
        serv={"type":servicio.type,"port":servicio.port,
        "weight":servicio.weight,"priority":servicio.priority,"server":servicio.server,"properties":properties,
        "interface_index":servicio.interface_index,"vulnerabilities":consultarVulnerabilidades(servicio.type,servicio.name)}
        ipsPort=str(servicio.parsed_addresses()[0])+":"+str(servicio.port)
        serviciosPorIPs[ipsPort]={str(servicio.name):serv}
        
#guardamos en ./json/UPnP.json el json creado para hacer las pruebas de la aplicación
with open("./jsons/mDNS.json","w") as f:
    json.dump(mDNSDict, f)
print(mDNSDict)
print("----------------------------------------------------------------------------\n\n")
#especificamos método de envío, url, etc
response=enviar(mDNSDict,"mDNS")

#mostramos el código de estado y la respuesta recibida
print(response.status_code)
print(response.text)





