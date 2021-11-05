from zeroconf import ServiceBrowser, Zeroconf, ZeroconfServiceTypes
import socket
import time

import json
import requests

def enviar(j,peticion):
    jsonToSend={"Peticion":peticion, "info":j}
    jsonToSend=json.dumps(jsonToSend)
    url="http://localhost/ExploracionIoT/controlador.php"
    return requests.post(url, data=jsonToSend)

class MyListener:

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed\n" % (name))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            #print("Service %s added, service info: %s" % (name, info))
            print("Type "+info.type)
            print("Service "+info.name+" port "+str(info.port))
            #devuelve la IPv4 y la IPv6
            print("Weight "+str(info.weight))
            print("Priority "+str(info.priority))
            print("Properties ")
            properties=info.properties
            print(properties)
            #prueba de acceso a atributos de las propiedades
            for prop in info.properties:
                print(str(prop)+" : "+str(properties[prop]))
            print("server "+info.server)
            print("host_ttl "+str(info.host_ttl))
            print("other_ttl "+str(info.other_ttl))
            print("interface_index "+str(info.interface_index))
            print("dir")
            print(info.parsed_addresses())
            print("\n")
            arrayServicios.append(info)

arrayServicios=[]
zeroconf = Zeroconf()
listener = MyListener()
print("browser")
#El ServiceBrowser crea un hilo, el cual está 5 segundos buscando servicios, hasta que
#el hilo principal detiene este hilo.
browser = ServiceBrowser(zeroconf,list(ZeroconfServiceTypes.find(zc=zeroconf)),listener)
time.sleep(3)
browser.cancel()
print(arrayServicios)
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
            "interface_index":servicio.interface_index}
            serviciosPorIPs[ips][str(servicio.name)]=serv
        break
        print("xd")
    if not anyadido:
        serv={"type":servicio.type,"port":servicio.port,
        "weight":servicio.weight,"priority":servicio.priority,"server":servicio.server,"properties":properties,
        "interface_index":servicio.interface_index}
        serviciosPorIPs[servicio.parsed_addresses()[0]]={str(servicio.name):serv}
        
print("dict:\n\n")
print(serviciosPorIPs)
for a in serviciosPorIPs:
    print(" "+str(a))
    for b in serviciosPorIPs[a]:
        print("     "+str(b))

#guardamos en ./json/UPnP.json el json creado para hacer las pruebas de la aplicación
with open("./jsons/mDNS.json","w") as f:
    json.dump(mDNSDict, f)
print("----------------------------------------------------------------------------\n\n")
#especificamos método de envío, url, etc
response=enviar(mDNSDict,"mDNS")

#mostramos el código de estado y la respuesta recibida
print(response.status_code)
print(response.text)


#Falta la parte de enviar al json

#Para cambiar las keys:
#dictionary[new_key] = dictionary.pop(old_key)

#Para pasar de dict a json:
#r = json.dumps(r)


