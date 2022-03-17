from wsdiscovery.discovery import ThreadedWSDiscovery as WSD
import Vulnerabilidades

class WSDiscovery:
    vul = None

    def consultarVulnerabilidades(self, XAddrs):
        ip=XAddrs.split("/")[2].split(":")[0]

        for i in range(3):
            pos = XAddrs.find("/")
            XAddrs = XAddrs[pos + 1:]
        XAddrs = XAddrs.replace("_", " ").replace("/", " ");
        return self.vul.consultarVulnerabilidades(XAddrs,ip)
    def obtenerServicios(self, dispositivos):
        self.vul=Vulnerabilidades.Vulnerabilidades(dispositivos)

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
                    "MetadataVersion":str(service.getMetadataVersion()),"Scopes":scopes,"Types":types,"XAddrs":XAddrs, "Vulnerabilities":self.consultarVulnerabilidades(XAddrs)}
            for ipServicio in serviciosPorIPs:
                if ipServicio==ipPuerto:
                    anyadido=True
                    serviciosPorIPs[ipPuerto][XAddrs] = serv
            if not anyadido:
                serviciosPorIPs[ipPuerto] = {XAddrs: serv}
        return WSDict





















