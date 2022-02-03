from zeroconf import IPVersion, ServiceBrowser, Zeroconf, ZeroconfServiceTypes, DNSQuestionType
import time
import datetime
import requests

arrayServicios = []


# Método para enviar peticiones al servidor web
class MyListener:
    def remove_service(self, zeroconf, type, name):
        print("Service %s removed\n" % (name))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            arrayServicios.append(info)

    def update_service(self):
        print("servicio actualizado")


class MDNS:
    # Método para obtener vulnerabilidades del servicio
    def consultarVulnerabilidades(tipoServicio, nombreServicio):
        url = "https://services.nvd.nist.gov/rest/json/cves/1.0/"
        tipoServicioReducido = tipoServicio.split("_")[1].split("_")[0].split(".")[0].replace("-", " ")
        tipoServicioReducido = tipoServicioReducido.upper()

        # print(tipoServicioReducido)

        if (len(tipoServicioReducido) >= 3 and tipoServicioReducido != 'HTTP'):
            # Selecciono las vulnerabilidades encontradas en los últimos 3 meses en los servicios:
            fecha = datetime.datetime.now()
            fechaAhora = fecha.strftime("%Y-%m-%dT%H:%M:%S:000 UTC-00:00")
            fechaHace120dias = fecha - datetime.timedelta(days=120)
            fechaHace120dias = fechaHace120dias.strftime("%Y-%m-%dT%H:%M:%S:000 UTC-00:00")

            jsonVulnerabil = {"keyword": tipoServicioReducido, "resultsPerPage": 40, "pubStartDate": fechaHace120dias,
                              "pubEndDate": fechaAhora}

            r = requests.get(url, params=jsonVulnerabil)
            jsonVul = r.json()
            # este if es para sí con la anterior búsqueda no ha encontrado vulnerabilidades
            if (jsonVul["totalResults"] == 0):
                # print("Hay que generalizar las vulnerabilidades")
                jsonVulnerabil = {"keyword": tipoServicioReducido, "resultsPerPage": 10}
                r = requests.get(url, params=jsonVulnerabil)
                return r.json()
            else:
                return r.json()
        else:
            # este else es para si no puede encontrar vulnerabilidades. En este caso, se crea un result vacío
            # print("No ha sido posible encontrar vulnerabilidades")
            fecha = datetime.datetime.now()
            fechaAhora = fecha.strftime("%Y-%m-%dT%H:%M:%SZ")
            return {"resultsPerPage": 0, "startIndex": 0, "totalResults": 0, "result": {}};

    # En esta clase se manejan los eventos del serviceBrowser

    def obtenerServicios(self):
        zeroconf = Zeroconf(ip_version=IPVersion.V4Only, unicast=False)
        listener = MyListener()
        print("browser")
        # El ServiceBrowser crea un hilo, el cual está 3 segundos buscando servicios, hasta que el hilo principal cierre el ServiceBrowser
        # el hilo principal detiene este hilo.
        print("lista servicios encontrados:")
        serviciosEncontrados = list(ZeroconfServiceTypes.find(zc=zeroconf))
        browser = ServiceBrowser(zeroconf, serviciosEncontrados, listener, question_type=DNSQuestionType.QM)
        time.sleep(5)
        browser.cancel()
        print(arrayServicios)
        # se ordenan los servicios por IPs en un diccionario
        serviciosPorIPs = {}
        mDNSDict = {"mDNS": serviciosPorIPs}
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
                            "vulnerabilities": self.consultarVulnerabilidades(servicio.type, servicio.name)}
                    serviciosPorIPs[ipsPort][str(servicio.name)] = serv
                    break
            if not anyadido:
                serv = {"type": servicio.type, "port": servicio.port,
                        "weight": servicio.weight, "priority": servicio.priority, "server": servicio.server,
                        "properties": properties,
                        "interface_index": servicio.interface_index,
                        "vulnerabilities": self.consultarVulnerabilidades(servicio.type, servicio.name)}
                ipsPort = str(servicio.parsed_addresses()[0]) + ":" + str(servicio.port)
                serviciosPorIPs[ipsPort] = {str(servicio.name): serv}
        return mDNSDict
