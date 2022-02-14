
from wsdiscovery.discovery import ThreadedWSDiscovery as WSD

class WSDiscovery:

    def consultarVulnerabilidades(self):
        return []
    def obtenerServicios(self):
        #Se crea un objeto ThreadedWSDiscovery, y se comienza la búsqueda de servicios
        wsd = WSD()
        wsd.start()
        services = wsd.searchServices()
        #Se ordenan los servicios por IPs
        serviciosPorIPs = {}
        WSDict={"WS-Discovery": serviciosPorIPs}
        for service in services:
            anyadido=False
            XAddrs=str(service.getXAddrs())
            ipPuerto=XAddrs.split("/")[2]
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
                    "MetadataVersion":str(service.getMetadataVersion()),"Scopes":scopes,"Types":types,"XAddrs":XAddrs, "Vulnerabilities":self.consultarVulnerabilidades()}
            for ipServicio in serviciosPorIPs:
                if ipServicio==ipPuerto:
                    anyadido=True
                    serviciosPorIPs[ipPuerto][XAddrs] = serv
            if not anyadido:
                serviciosPorIPs[ipPuerto] = {XAddrs: serv}
        return WSDict





















