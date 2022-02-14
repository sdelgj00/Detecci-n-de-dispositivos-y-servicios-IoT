import json
import requests
from modulos.UPnP import UPnP
from modulos.Nmap import Nmap
from modulos.mDNS import MDNS
from modulos.WSDiscovery import WSDiscovery
from Constantes import Constantes

Dispositivos={}
def guardarEnArchivo(dir, dict):
    # guardamos en ./json/UPnP.json el json creado para hacer las pruebas de la aplicación
    with open(dir, "w") as f:
        json.dump(dict, f)

def enviar(j, peticion):
    jsonToSend = {"Peticion": peticion, "info": j}
    jsonToSend = json.dumps(jsonToSend)
    jsonToSend = jsonToSend.replace("'", "''");
    # url="https://exploracion-iot.000webhostapp.com/controlador.php"
    url = "http://localhost/ExploracionIoT/controlador.php"
    return requests.post(url, data=jsonToSend)

if __name__ == '__main__':
    """hay que pasar la direccion de búsqueda como parámetro(192.168.1.0/24), además del tipo de búsqueda al 
    método obtener dispositivos del objeto nmap"""
    cons=Constantes()
    print(cons.ExploradorIoT)
    nmap=Nmap()
    upnp=UPnP()
    mdns=MDNS()
    wsdiscovery=WSDiscovery()
    """try:
        print("hola")
    except Exception as a:
        print(a)"""
    #Exploracion con nmap
    Dispositivos=nmap.obtenerDispositivos("10.130.16.0/21","A")
    guardarEnArchivo("./jsons/Nmap.json", Dispositivos)
    print()
    print(Dispositivos)
    print("------------------------------------")

    #Exploracion UPnP
    ServiciosUPnP=upnp.obtenerServicios(Dispositivos)
    guardarEnArchivo("./jsons/UPnP.json",ServiciosUPnP)
    print(ServiciosUPnP)
    print("------------------------------------")

    #Exploracion mDNS
    ServiciosMDNS=mdns.obtenerServicios(Dispositivos)
    guardarEnArchivo("./jsons/mDNS.json",ServiciosMDNS)
    print(ServiciosMDNS)
    print("------------------------------------")

    #Exploracion WS-Discovery
    ServiciosWSDiscovery=wsdiscovery.obtenerServicios()
    guardarEnArchivo("./jsons/WS-Discovery.json",ServiciosWSDiscovery)
    print(ServiciosWSDiscovery)
    print("------------------------------------")

    #Union de toda la informacion para enviarla al servidor
    DictEnvio={"Nmap":Dispositivos,"UPnP":ServiciosUPnP,"mDNS":ServiciosMDNS,"WS-Discovery":ServiciosWSDiscovery}
    print(DictEnvio)
    cositas=enviar(DictEnvio, "All")
    print(cositas.text)



