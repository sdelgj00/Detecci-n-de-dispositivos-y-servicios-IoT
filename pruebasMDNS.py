from zeroconf import ServiceBrowser, Zeroconf, ZeroconfServiceTypes
import socket
import time

import json
import requests

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
MDNSXml=etree.Element("mDNS")
serviciosPorIPs={}
for servicio in arrayServicios:
    anyadido=False
    for ips in serviciosPorIPs:
        if ips==servicio.parsed_addresses()[0]:
            anyadido=True
            ips.append(servicio)
            break
    if not anyadido:
        serviciosPorIPs[servicio.parsed_addresses()[0]]=[]
        serviciosPorIPs[servicio.parsed_addresses()[0]].append(servicio)
print("dict:\n\n")
print(serviciosPorIPs)
for a in serviciosPorIPs:
    print(" "+str(a))
    for b in serviciosPorIPs[a]:
        print("     "+str(b))
archivoXml=etree.ElementTree(MDNSXml)
archivoXml.write("./xmls/mDNS.xml")
#Falta la parte de enviar al json

#Para cambiar las keys:
#dictionary[new_key] = dictionary.pop(old_key)

#Para pasar de dict a json:
#r = json.dumps(r)


