from zeroconf import IPVersion, ServiceBrowser, Zeroconf, ZeroconfServiceTypes, DNSQuestionType
import time
import Vulnerabilidades
import logging

arrayServicios = []
update=0
vul=None

# Método para enviar peticiones al servidor web
class MyListener:
    def remove_service(self, zeroconf, type, name):
        print("Service %s removed\n" % (name))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            arrayServicios.append(info)

    def update_service(self,a,b,c):
        update+1


class MDNS:
    # Método para obtener vulnerabilidades del servicio
    Dispositivos={}

    def obtenerCPE(self,IP):
        for i in self.Dispositivos['Nmap']:
            if i == IP:
                try:
                    return self.Dispositivos['Nmap'][IP]['osmatch'][0]['osclass'][0]['cpe'][0]+'*'
                except:
                    return ''
        return ''
    def consultarVulnerabilidades(self,tipoServicio, nombreServicio, ip):
        tipoServicioReducido = tipoServicio.split("_")[1].split("_")[0].split(".")[0].replace("-", " ")
        tipoServicioReducido = tipoServicioReducido.upper()
        return self.vul.consultarVulnerabilidades(tipoServicioReducido,ip)
    # En esta clase se manejan los eventos del serviceBrowser

    def obtenerServicios(self, dispositivos):
        self.vul=Vulnerabilidades.Vulnerabilidades(dispositivos)
        zeroconf = Zeroconf(ip_version=IPVersion.V4Only, unicast=False)
        listener = MyListener()
        # El ServiceBrowser crea un hilo, el cual está 3 segundos buscando servicios, hasta que el hilo principal cierre el ServiceBrowser
        # el hilo principal detiene este hilo.
        serviciosEncontrados = list(ZeroconfServiceTypes.find(zc=zeroconf))
        browser = ServiceBrowser(zeroconf, serviciosEncontrados, listener, question_type=DNSQuestionType.QM)
        time.sleep(5)
        browser.cancel()
        # se ordenan los servicios por IPs en un diccionario
        serviciosPorIPs = {}
        mDNSDict = {"mDNS": serviciosPorIPs}

        #log servicios encontrados
        serviciosLog="servicios mDNS encontrados:\n"
        for servicio in arrayServicios:
            serviciosLog+=servicio.type+"\n"
        logging.info(serviciosLog)

        for servicio in arrayServicios:
            anyadido = False
            properties = {}
            servicio.properties
            for a in servicio.properties:
                clave = str(a)
                clave = clave[2:len(clave) - 1]
                valor = str(servicio.properties[a])
                valor = valor[2:len(valor) - 1]
                properties[clave] = valor
            for ips in serviciosPorIPs:
                ipsPort = str(servicio.parsed_addresses()[0]) + ":" + str(servicio.port)
                if ips == ipsPort:
                    anyadido = True
                    serv = {"type": servicio.type, "port": servicio.port,
                            "weight": servicio.weight, "priority": servicio.priority, "server": servicio.server,
                            "properties": properties,
                            "interface_index": servicio.interface_index,
                            "vulnerabilities": self.consultarVulnerabilidades(servicio.type, servicio.name, ipsPort.split(':')[0])}
                    serviciosPorIPs[ipsPort][str(servicio.name)] = serv
                    break
            if not anyadido:
                serv = {"type": servicio.type, "port": servicio.port,
                        "weight": servicio.weight, "priority": servicio.priority, "server": servicio.server,
                        "properties": properties,
                        "interface_index": servicio.interface_index,
                        "vulnerabilities": self.consultarVulnerabilidades(servicio.type, servicio.name, str(servicio.parsed_addresses()[0]))}
                ipsPort = str(servicio.parsed_addresses()[0]) + ":" + str(servicio.port)
                serviciosPorIPs[ipsPort] = {str(servicio.name): serv}
        return mDNSDict

