import upnpy
from lxml import etree
if __name__== "__main__":
    #Añadimos el UPnP al xml
    UPnPXml=etree.Element("UPnP")
    upnp=upnpy.UPnP()
    devices=upnp.discover()
    #añadimos los dispositivos al xml
    for device in devices:
        deviceName=str(device)
        deviceName=deviceName.replace("Device <","")
        deviceName=deviceName.replace(">","")
        deviceXml=etree.SubElement(UPnPXml,deviceName, IP=device.address[0], port=str(device.address[1]))
        servicesXml=etree.SubElement(deviceXml,"services")
        #añadimos los servicios de cada dispositivo al xml
        for service in device.get_services():
            #el proceso de hacer el split es para obtener el nombre y el id del servicio
            serviceTXT=str(service)
            dividedService=serviceTXT.split()
            serviceXml=etree.SubElement(servicesXml,dividedService[1].replace("(","").replace(")",""),
            ID=dividedService[2].replace("id=","").replace('"',"").replace(">",""),
            SCPD=service.scpd_url, ControlUrl=service.control_url, EventUrl=service.event_sub_url,
            BaseUrl=service.base_url)
            actions=service.get_actions()
            actionsXml=etree.SubElement(serviceXml, "actions")
            #añadimos las acciones de cada servicio
            for action in actions:
                actionXml=etree.SubElement(actionsXml,action.name)
                inputArgs=action.get_input_arguments()
                outputArgs=action.get_output_arguments()
                #añadimos los argumentos de entrada a la acción
                inputArgsXml=etree.SubElement(actionXml, "input_args")
                for inputArg in inputArgs:
                    allowedVals=inputArg['allowed_value_list']
                    allowedValsString=""
                    for vals in allowedVals:
                        allowedValsString+=","+vals
                    allowedValsString=allowedValsString[1:len(allowedValsString)]
                    inputArgXml=etree.SubElement(inputArgsXml,inputArg['name'], dataType=inputArg['data_type'],
                    allowedValueList=allowedValsString)
                #añadimos los argumentos de salida a la acción
                outputArgsXml=etree.SubElement(actionXml, "output_args")
                for outputArg in outputArgs:
                    allowedVals=outputArg['allowed_value_list']
                    allowedValsString=""
                    for vals in allowedVals:
                        allowedValsString+=","+vals
                    allowedValsString=allowedValsString[1:len(allowedValsString)]
                    outputArgXml=etree.SubElement(outputArgsXml,outputArg['name'], dataType=outputArg['data_type'],
                    allowedValueList=allowedValsString)
    #escribimos en el archivo ./xmls/UPnP.xml el xml correspondiente al escaneo mediante el protocolo UPnP
    archivoXml=etree.ElementTree(UPnPXml)
    archivoXml.write("./xmls/UPnP.xml")
   


