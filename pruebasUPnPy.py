import upnpy
from lxml import etree
if __name__== "__main__":
    #Añadimos el UPnP al xml
    UPnPXml=etree.Element("UPnP")
    upnp=upnpy.UPnP()
    dispositivos=upnp.discover()
    print(dispositivos[0].address)
    print((dispositivos[0].response))
    print(dispositivos[0])
    #print(dispositivos[0].get_services()[1].service_id)
    print(dispositivos[0].get_services())
    print("hola")
    print(dispositivos[0].get_services()[0])
    print(dispositivos[0].get_services()[0].base_url)
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
            print("acciones")
            print(actions)
            actionsXml=etree.SubElement(servicioXml, "actions")
            #añadimos las acciones de cada servicio
            for action in actions:
                actionXml=etree.SubElement(actionsXml,action.name)
                inputArgsXml=etree.SubElement(actionXml, "input_args")
                inputArgs=action.get_input_arguments()
                outputArgs=action.get_output_arguments()
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
    archivoXml=etree.ElementTree(UPnPXml)
    archivoXml.write("./xmls/UPnP.xml")
    """IGD=dispositivos[0]
    print(IGD)
    print(IGD.get_services())
    servicio=IGD['WANIPConn1']
    print(servicio)
    print(servicio.get_actions())
    print(servicio.GetExternalIPAddress())
    print(servicio.GetStatusInfo.get_input_arguments())
    print(servicio.GetStatusInfo.get_output_arguments())
    print(servicio.GetStatusInfo())"""


