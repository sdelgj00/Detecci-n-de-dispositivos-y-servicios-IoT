import upnpy
import requests
import datetime
import Vulnerabilidades
import logging

class UPnP:
    vul = None

    def obtenerCPE(self,IP):
        for i in self.Dispositivos['Nmap']:
            if i == IP:
                try:
                    return self.Dispositivos['Nmap'][IP]['osmatch'][0]['osclass'][0]['cpe'][0]
                except:
                    return ''
        return ''
    def consultarVulnerabilidades(self,nombreServicio, ip):
        url = "https://services.nvd.nist.gov/rest/json/cves/1.0/"
        # Esto sirve para añadir espacios entre las palabras
        p = ""
        nombreServicio = nombreServicio.replace("_", " ").replace("-", " ")
        for l in range(0, len(nombreServicio)):
            if (l == len(nombreServicio)):
                p = p + nombreServicio[l]
            elif (l == 0):
                p = nombreServicio[l]
            elif (nombreServicio[l].isupper()):
                p = p + " " + nombreServicio[l]
            else:
                p = p + nombreServicio[l]
        pSeparados = p.split(" ")
        p = ""
        for l in pSeparados:
            if (l.isupper()):
                p = p + l
            else:
                p = p + " " + l
        return self.vul.consultarVulnerabilidades(p, ip)
    def obtenerServicios(self, dispositivos):
        self.vul=Vulnerabilidades.Vulnerabilidades(dispositivos)
        # Añadimos el UPnP al dict
        DevicesDict = {}
        UPnPDict = {"UPnP": DevicesDict}
        upnp = upnpy.UPnP()
        devices = upnp.discover()
        # añadimos los dispositivos al dict

        #log servicios encontrados
        serviciosLog = "servicios UPnP encontrados:\n"
        for device in devices:
            serviciosLog += str(device.address[0]) + ":" + str(device.address[1])+":\n"
            for service in device.get_services():
                serviceTXT = str(service)
                dividedService = serviceTXT.split()
                serviciosLog += "\t"+dividedService[1].replace("(", "").replace(")", "")+"\n"
        logging.info(serviciosLog)

        for device in devices:

            # print(device.get_friendly_name())
            deviceName = str(device)
            deviceName = deviceName.replace("Device <", "")
            deviceName = deviceName.replace(">", "")
            ServicesDict = {}
            # Esto es por si hay varios programas UPnP, los cuales corren en puertos distintos
            ipPuerto = str(device.address[0]) + ":" + str(device.address[1])
            DevicesDict[ipPuerto] = {"Name": deviceName, "port": str(device.address[1]), "services": ServicesDict}
            # añadimos los servicios de cada dispositivo al dict
            for service in device.get_services():
                # el proceso de hacer el split es para obtener el nombre y el id del servicio
                serviceTXT = str(service)
                dividedService = serviceTXT.split()
                ActionsDict = {}
                ServicesDict[dividedService[1].replace("(", "").replace(")", "")] = {
                    "ID": dividedService[2].replace("id=", "").replace('"', "").replace(">", ""),
                    "SCPD": service.scpd_url, "ControlUrl": service.control_url, "EventUrl": service.event_sub_url,
                    "BaseUrl": service.base_url, "actions": ActionsDict,
                    "vulnerabilities": self.consultarVulnerabilidades(dividedService[1].replace("(", "").replace(")", ""),str(device.address[0]))}
                actions = service.get_actions()
                # añadimos las acciones de cada servicio
                for action in actions:
                    ActionsDict[action.name] = {}
                    inputArgs = action.get_input_arguments()
                    outputArgs = action.get_output_arguments()
                    # añadimos los argumentos de entrada a la acción
                    inputArgsDict = {}
                    outputArgsDict = {}
                    ActionsDict[action.name]["input_args"] = inputArgsDict
                    ActionsDict[action.name]["output_args"] = outputArgsDict
                    for inputArg in inputArgs:
                        allowedVals = inputArg['allowed_value_list']
                        allowedValsString = ""
                        for vals in allowedVals:
                            allowedValsString += "," + vals
                        allowedValsString = allowedValsString[1:len(allowedValsString)]
                        inputArgsDict[inputArg["name"]] = {"dataType": inputArg['data_type'],
                                                           "allowedValueList": allowedValsString}
                    # añadimos los argumentos de salida a la acción
                    for outputArg in outputArgs:
                        allowedVals = outputArg['allowed_value_list']
                        allowedValsString = ""
                        for vals in allowedVals:
                            allowedValsString += "," + vals
                        allowedValsString = allowedValsString[1:len(allowedValsString)]
                        outputArgsDict[outputArg["name"]] = {"dataType": outputArg['data_type'],
                                                             "allowedValueList": allowedValsString}
                        outputArgDict = {"dataType": outputArg['data_type'], "allowedValueList": allowedValsString}

        return UPnPDict



