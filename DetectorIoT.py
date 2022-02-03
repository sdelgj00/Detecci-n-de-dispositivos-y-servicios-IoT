import json
import requests
from modulos.UPnP import UPnP
from modulos.Nmap import Nmap
from modulos.mDNS import MDNS
from modulos.WSDiscovery import WSDiscovery

def guardarEnArchivo(self, dir, dict):
    # guardamos en ./json/UPnP.json el json creado para hacer las pruebas de la aplicación
    with open(dir, "w") as f:
        json.dump(dict, f)
    print(dict)

def enviar(j, peticion):
    jsonToSend = {"Peticion": peticion, "info": j}
    jsonToSend = json.dumps(jsonToSend)
    jsonToSend = jsonToSend.replace("'", "''");
    # url="https://exploracion-iot.000webhostapp.com/controlador.php"
    url = "http://localhost/ExploracionIoT/controlador.php"
    return requests.post(url, data=jsonToSend)

if __name__ == '__main__':
    nmap=Nmap()
    upnp=UPnP()
    mdns=MDNS()
    wsdiscovery=WSDiscovery()
    print(nmap.obtenerDispositivos())