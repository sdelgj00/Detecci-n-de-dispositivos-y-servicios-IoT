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

#Método para obtener vulnerabilidades del dispositivo
#Habría que buscar por el nombre del servicio
def consultarVulnerabilidades(tipoServicio, nombreServicio):
    url="https://services.nvd.nist.gov/rest/json/cves/1.0/"
    tipoServicioReducido=tipoServicio.split("_")[1].split("_")[0].split(".")[0].split("-")[0]
    tipoServicioReducido=tipoServicioReducido.upper()
    #no hace falta usarlo pero podría hacer falta:
    cpeNormalizedName=nombreServicio.split(" (")[0].split(" -")[0]
    print(tipoServicioReducido)
    #esto lo he puesto igual que en el TFM para probar
    """if(len(nombreServicio)>=60):
        print("pato2")
        sonVulnerabil={"keyword":tipoServicioReducido,}
    else:
        print("pato")
        #cpe:/:"+"tp"+":"+"tp"
        jsonVulnerabil={"keyword":tipoServicioReducido,"cpeMatchString":"cpe:2.3:*:"+cpeNormalizedName}
        #        jsonVulnerabil={"keyword":tipoServicioReducido,"cpeMatchString":"cpe:/:"+cpeNormalizedName+":"+cpeNormalizedName} """
    print(len(tipoServicioReducido)<3)
    print(tipoServicioReducido!='HTTP')
    if(len(tipoServicioReducido)>=3 and tipoServicioReducido!='HTTP'):
        #Selecciono las vulnerabilidades encontradas en los últimos 3 meses en los servicios:
        print("fecha:")
        fecha=datetime.datetime.now()
        fechaAhora=fecha.strftime("%Y-%m-%dT%H:%M:%S:000 UTC-00:00")
        fechaHace120dias=fecha-datetime.timedelta(days=120)
        fechaHace120dias=fechaHace120dias.strftime("%Y-%m-%dT%H:%M:%S:000 UTC-00:00")
        #yyyy-MM-dd'T'HH:mm:ss:SSS z
        #2021-11-11'T'19:48:33:000 UTC-00:00
        #2016-01-01T00:00:00:000 UTC-00:00
        print(fechaAhora)
        print(fechaHace120dias)
        
        jsonVulnerabil={"keyword":tipoServicioReducido, "resultsPerPage":40,"pubStartDate": fechaHace120dias,
        "pubEndDate":fechaAhora}
        
        r=requests.get(url,params=jsonVulnerabil)
        print(r.url)
        print(r.status_code)
        print(r.text)
        return r.json()
    else:
        print("No ha sido posible encontrar vulnerabilidades")
        return  {"resultsPerPage": 0, "startIndex": 0, "totalResults": 0, "result": {"CVE_data_type": "CVE", "CVE_data_format": "MITRE",
                "CVE_data_version": "4.0", "CVE_data_timestamp": "2021-11-11T19:07Z", "CVE_Items": []}};

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
#El ServiceBrowser crea un hilo, el cual está 3 segundos buscando servicios, hasta que
#el hilo principal detiene este hilo.
#list(ZeroconfServiceTypes.find(zc=zeroconf))
#list(ZeroconfServiceTypes.find(zc=zeroconf))
#["_wled._tcp.local.","Android.local."]
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
    print(servicio.properties)
    servicio.properties
    for a in servicio.properties:
        print("ii")
        clave=str(a)
        clave=clave[2:len(clave)-1]
        print(a)
        print(clave)
        valor=str(servicio.properties[a])
        valor=valor[2:len(valor)-1]
        properties[clave]=valor
        print(valor)
    print("props")
    print(properties)
    for ips in serviciosPorIPs:
        if ips==servicio.parsed_addresses()[0]:
            anyadido=True
            
            serv={"type":servicio.type,"port":servicio.port,
            "weight":servicio.weight,"priority":servicio.priority,"server":servicio.server,"properties":properties,
            "interface_index":servicio.interface_index,"vulnerabilities":consultarVulnerabilidades(servicio.type, servicio.name)}
            serviciosPorIPs[ips][str(servicio.name)]=serv
        break
        print("xd")
    if not anyadido:
        serv={"type":servicio.type,"port":servicio.port,
        "weight":servicio.weight,"priority":servicio.priority,"server":servicio.server,"properties":properties,
        "interface_index":servicio.interface_index,"vulnerabilities":consultarVulnerabilidades(servicio.type,servicio.name)}
        serviciosPorIPs[servicio.parsed_addresses()[0]]={str(servicio.name):serv}
        
#guardamos en ./json/UPnP.json el json creado para hacer las pruebas de la aplicación
with open("./jsons/mDNS.json","w") as f:
    json.dump(mDNSDict, f)
print("----------------------------------------------------------------------------\n\n")
#especificamos método de envío, url, etc
response=enviar(mDNSDict,"mDNS")

#mostramos el código de estado y la respuesta recibida
print(response.status_code)
print(response.text)





