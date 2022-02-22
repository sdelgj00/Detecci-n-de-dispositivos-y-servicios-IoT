import json
import requests
from modulos.UPnP import UPnP
from modulos.Nmap import Nmap
from modulos.mDNS import MDNS
from modulos.WSDiscovery import WSDiscovery
import Constantes
import argparse

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
def explorarYGuardar(archivo,dict):
    guardarEnArchivo(archivo, dict)
    print()
    print(dict)
    print("------------------------------------------------------------------")

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Explorador de red local (IoT)')
    parser.add_argument("--IP",type=str, default=None, help="IP de exploración. Ejemplo: 192.168.8.0/24")
    parser.add_argument("--EL",type=str, default=None, help="Nivel de exploración: F más bajo y A más alto")
    parser.add_argument("--v", help="(Opcional) Aumenta la información mostrada por el programa",action="store_true")

    args=parser.parse_args()
    if not args.IP or not args.EL:
        print(parser.print_help())
        exit(-1)
    """hay que pasar la direccion de búsqueda como parámetro(192.168.1.0/24), además del tipo de búsqueda al 
    método obtener dispositivos del objeto nmap"""
    print(Constantes.ExploradorIoT)
    print("------------------------------------------------------------------")
    nmap=Nmap()
    upnp=UPnP()
    mdns=MDNS()
    wsdiscovery=WSDiscovery()
    """try:
        print("hola")
    except Exception as a:
        print(a)"""

    #Exploracion con nmap
    try:
        print(Constantes.tituloExploracion("nmap"))
        Dispositivos=nmap.obtenerDispositivos(args.IP,args.EL)
        explorarYGuardar("./jsons/Nmap.json",Dispositivos)
    except Exception as a:
        print("Problemas al realizar la exploración nmap: "+args.IP+" "+args.EL)
        print()
        print(a)
        exit(-1)

    #Exploracion UPnP
    try:
        print(Constantes.tituloExploracion("upnp"))
        ServiciosUPnP=upnp.obtenerServicios(Dispositivos)
        explorarYGuardar("./jsons/UPnP.json",ServiciosUPnP)
    except Exception as a:
        print("Problemas al realizar la exploración UPnP")
        print()
        print(a)
        exit(-1)

    #Exploracion mDNS
    try:
        print(Constantes.tituloExploracion("mdns"))
        ServiciosMDNS=mdns.obtenerServicios(Dispositivos)
        explorarYGuardar("./jsons/mDNS.json",ServiciosMDNS)
    except Exception as a:
        print("Problemas al realizar la exploración mDNS")
        print()
        print(a)
        exit(-1)

    #Exploracion WS-Discovery
    try:
        print(Constantes.tituloExploracion("wsdiscovery"))
        ServiciosWSDiscovery=wsdiscovery.obtenerServicios()
        explorarYGuardar("./jsons/WS-Discovery.json",ServiciosWSDiscovery)
    except Exception as a:
        print("Problemas al realizar la exploración WS-Discovery")
        print()
        print(a)
        exit(-1)
    print("------------------------------------------------------------------")
    print("------------------------------------------------------------------")
    print("------------------------------------------------------------------")

    #Union de toda la informacion para enviarla al servidor
    DictEnvio={"Nmap":Dispositivos,"UPnP":ServiciosUPnP,"mDNS":ServiciosMDNS,"WS-Discovery":ServiciosWSDiscovery}
    if args.v:
        print(DictEnvio)
    cositas=enviar(DictEnvio, "All")
    if args.v:
        print(cositas.text)



