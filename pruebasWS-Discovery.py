import json
import requests
from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from wsdiscovery import QName, Scope


from wsdiscovery.publishing import ThreadedWSPublishing as WSPublishing
    # Define type, scope & address of service
ttype1 = QName("http://www.onvif.org/ver10/device/wsdl", "Device")
ttype2 = QName("http://www.onvif.org/ver10/device/wsdl", "Sium")
scope1 = Scope("onvif://www.onvif.org/Model")
scope2 = Scope("onvif://www.onvif.org/ModelJaja")
xAddr1 = "https://192.168.1.101:8080/abc"
xAddr2="https://192.168.1.101:69/abc"
xAddr3="https://192.168.1.101:69/xd"
    # Publish the service
wsp = WSPublishing()
wsp.start()
wsp.publishService(types=[ttype1, ttype2], scopes=[scope1,scope2], xAddrs=[xAddr1])

wsp2 = WSPublishing()
wsp2.start()
wsp2.publishService(types=[ttype1], scopes=[scope1], xAddrs=[xAddr2])

wsp3 = WSPublishing()
wsp3.start()
wsp3.publishService(types=[ttype1], scopes=[scope1], xAddrs=[xAddr3])

def enviar(j,peticion):
    jsonToSend={"Peticion":peticion, "info":j}
    jsonToSend=json.dumps(jsonToSend)
    url="https://exploracion-iot.000webhostapp.com/controlador.php"
    #url="http://localhost/ExploracionIoT/controlador.php"
    return requests.post(url, data=jsonToSend)
def consultarVulnerabilidades():
    return []

wsd = WSDiscovery()
wsd.start()
services = wsd.searchServices()
for service in services:
    print("service: "+str(service))
    print("EPR: "+service.getEPR())
    print("InstanceId: "+str(service.getInstanceId()))
    print("MessageNumber: "+str(service.getMessageNumber()))
    print("MetadataVersion: "+str(service.getMetadataVersion()))
    print("Scopes: "+str(service.getScopes()))#list
    for scope in service.getScopes():
        print("---scope MatchBy :"+scope.getMatchBy())
        print("---scope QuotedValue :"+scope.getQuotedValue())
        print("---scope Value :"+scope.getValue())
    print("Types: "+str(service.getTypes()))#list
    for type in service.getTypes():
        print("---type:"+str(type))
    print("XAddrs: "+str(service.getXAddrs()))
    print("----------------------------------")
wsd.stop()


serviciosPorIPs = {}
WSDict={"WS-Discovery": serviciosPorIPs}
for service in services:
    anyadido=False
    XAddrs=str(service.getXAddrs())
    ipPuerto=XAddrs.split("/")[2]
    print(ipPuerto)
    scopes={}
    i=0
    for scope in service.getScopes():
        scopeConcreto={}
        scopeConcreto["MatchBy"]=scope.getMatchBy()
        scopeConcreto["QuotedValue"]=scope.getQuotedValue()
        scopeConcreto["Value"]=scope.getValue()
        scopes[i]=scopeConcreto
        i+=1
    types={}
    i=0
    for type in service.getTypes():
        types[i]=str(type)
        i+=1
    XAddrs=str(service.getXAddrs())[2:-2]
    serv={"EPR":str(service.getEPR()),"InstanceId":str(service.getInstanceId()),"MessageNumber":str(service.getMessageNumber()),
            "MetadataVersion":str(service.getMetadataVersion()),"Scopes":scopes,"Types":types,"XAddrs":XAddrs, "Vulnerabilities":consultarVulnerabilidades()}
    for ipServicio in serviciosPorIPs:
        if ipServicio==ipPuerto:
            anyadido=True
            serviciosPorIPs[ipPuerto][XAddrs] = serv
    if not anyadido:
        serviciosPorIPs[ipPuerto] = {XAddrs: serv}
print(WSDict)
print("----------------------------------------------------------------------------\n\n")
# especificamos método de envío, url, etc
response = enviar(WSDict, "WS-Discovery")

# mostramos el código de estado y la respuesta recibida
print(response.status_code)
print(response.text)




















