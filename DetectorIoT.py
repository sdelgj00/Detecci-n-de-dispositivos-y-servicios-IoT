import json
import requests
from modulos.UPnP import UPnP
from modulos.Nmap import Nmap
from modulos.mDNS import MDNS
from modulos.WSDiscovery import WSDiscovery
import Constantes
import argparse
import logging
from traceback import format_exc



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
def logError(msg, a):
    print(msg)
    print()
    logging.error(msg)
    logging.error(a)

if __name__ == '__main__':
    logging.basicConfig(filename='logs.txt',format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)
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
        logError("Problemas al realizar la exploración nmap: "+args.IP+" "+args.EL,format_exc())
        exit(-1)

    #Exploracion UPnP
    try:
        print(Constantes.tituloExploracion("upnp"))
        ServiciosUPnP=upnp.obtenerServicios(Dispositivos)
        explorarYGuardar("./jsons/UPnP.json",ServiciosUPnP)
    except Exception as a:
        logError("Problemas al realizar la exploración UPnP",format_exc())
        exit(-1)

    #Exploracion mDNS
    try:
        print(Constantes.tituloExploracion("mdns"))
        ServiciosMDNS=mdns.obtenerServicios(Dispositivos)
        explorarYGuardar("./jsons/mDNS.json",ServiciosMDNS)
    except Exception as a:
        logError("Problemas al realizar la exploración mDNS",format_exc())
        exit(-1)

    #Exploracion WS-Discovery
    try:
        print(Constantes.tituloExploracion("wsdiscovery"))
        ServiciosWSDiscovery=wsdiscovery.obtenerServicios()
        explorarYGuardar("./jsons/WS-Discovery.json",ServiciosWSDiscovery)
    except Exception as a:
        logError("Problemas al realizar la exploración WS-Discovery",format_exc())
        exit(-1)
    print("------------------------------------------------------------------")
    print("------------------------------------------------------------------")
    print("------------------------------------------------------------------")
    logging.info("Completado escaneo")
    #Union de toda la informacion para enviarla al servidor
    DictEnvio={"Nmap":Dispositivos,"UPnP":ServiciosUPnP,"mDNS":ServiciosMDNS,"WS-Discovery":ServiciosWSDiscovery}
    if args.v:
        print(DictEnvio)
    try:
        cositas=enviar(DictEnvio, "All")
    except Exception as a:
        logError("No se ha podido contactar con el servidor",format_exc())
        exit(-1)
    if args.v:
        print(cositas.text)



