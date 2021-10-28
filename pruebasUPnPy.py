import upnpy
from lxml import etree
if __name__== "__main__":
    #Añadimos el UPnP al xml
    UPnPXml=etree.Element("UPnP")
    upnp=upnpy.UPnP()
    dispositivos=upnp.discover()
    #añadimos los dispositivos al xml
    for dispositivo in dispositivos:
        nombreDispositivo=str(dispositivo)
        nombreDispositivo=nombreDispositivo.replace("Device <","")
        nombreDispositivo=nombreDispositivo.replace(">","")
        dispositivoXml=etree.SubElement(UPnPXml,nombreDispositivo, IP=dispositivo.address[0], port=str(dispositivo.address[1]))
        serviciosXml=etree.SubElement(dispositivoXml,"services")
        #añadimos los servicios de cada dispositivo al xml
        for servicio in dispositivo.get_services():
            servicioTXT=str(servicio)
            servicioDividido=servicioTXT.split()
            servicioXml=etree.SubElement(serviciosXml,servicioDividido[1].replace("(","").replace(")",""),
            ID=servicioDividido[2].replace("id=","").replace('"',"").replace(">",""),
            SCPD=servicio.scpd_url, ControlUrl=servicio.control_url, EventUrl=servicio.event_sub_url,
            BaseUrl=servicio.base_url)
            actions=servicio.get_actions()
            actionsXml=etree.SubElement(servicioXml, "actions")
            #añadimos las acciones de cada servicio
            for action in actions:
                actionXml=etree.SubElement(actionsXml,action.name)
                inputArgs=action.get_input_arguments()
                outputArgs=action.get_output_arguments()
                #añadimos los argumentos de entrada a la acción
                inputArgsXml=etree.SubElement(actionXml, "input_args")
                for inputArg in inputArgs:
                    print(inputArg['name'])
                    print(inputArg['data_type'])
                    print(inputArg['allowed_value_list'])
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
                    print(outputArg['name'])
                    print(outputArg['data_type'])
                    print(outputArg['allowed_value_list'])
                    allowedVals=outputArg['allowed_value_list']
                    allowedValsString=""
                    for vals in allowedVals:
                        allowedValsString+=","+vals
                    allowedValsString=allowedValsString[1:len(allowedValsString)]
                    outputArgXml=etree.SubElement(outputArgsXml,outputArg['name'], dataType=outputArg['data_type'],
                    allowedValueList=allowedValsString)
                print(action.get_input_arguments())
                print(action.get_output_arguments())
                print(action.name)
    #escribimos en el archivo ./xmls/UPnP.xml el xml correspondiente al escaneo mediante el protocolo UPnP
    archivoXml=etree.ElementTree(UPnPXml)
    archivoXml.write("./xmls/UPnP.xml")
   


