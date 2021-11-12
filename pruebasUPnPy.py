import upnpy

import json
import requests

#Método para enviar peticiones al servidor web
def enviar(j,peticion):
    jsonToSend={"Peticion":peticion, "info":j}
    jsonToSend=json.dumps(jsonToSend)
    #url="https://exploracion-iot.000webhostapp.com/controlador.php"
    url="http://localhost/ExploracionIoT/controlador.php"
    return requests.post(url, data=jsonToSend)

#Añadimos el UPnP al dict
DevicesDict={}
UPnPDict={"UPnP": DevicesDict} 
upnp=upnpy.UPnP()
devices=upnp.discover()
#añadimos los dispositivos al dict
for device in devices:
    print("iii")
    deviceName=str(device)
    deviceName=deviceName.replace("Device <","")
    deviceName=deviceName.replace(">","")
    ServicesDict={}
    #Esto es por si hay varios programas UPnP, los cuales corren en puertos distintos
    ipPuerto=str(device.address[0])+":"+str(device.address[1])
    DevicesDict[ipPuerto]={"Name":deviceName,"port":str(device.address[1]),"services":ServicesDict}
    #añadimos los servicios de cada dispositivo al dict
    for service in device.get_services():
        #el proceso de hacer el split es para obtener el nombre y el id del servicio
        serviceTXT=str(service)
        dividedService=serviceTXT.split()
        ActionsDict={}
        ServicesDict[dividedService[1].replace("(","").replace(")","")]={"ID":dividedService[2].replace("id=","").replace('"',"").replace(">",""),
        "SCPD":service.scpd_url, "ControlUrl":service.control_url, "EventUrl":service.event_sub_url, "BaseUrl":service.base_url, "actions":ActionsDict}
        actions=service.get_actions()
        #añadimos las acciones de cada servicio
        for action in actions:
            ActionsDict[action.name]={}                                     
            inputArgs=action.get_input_arguments()
            outputArgs=action.get_output_arguments()
            #añadimos los argumentos de entrada a la acción
            inputArgsDict={}
            outputArgsDict={}
            ActionsDict[action.name]["input_args"]=inputArgsDict
            ActionsDict[action.name]["output_args"]=outputArgsDict
            for inputArg in inputArgs:
                allowedVals=inputArg['allowed_value_list']
                allowedValsString=""
                for vals in allowedVals:
                    allowedValsString+=","+vals
                allowedValsString=allowedValsString[1:len(allowedValsString)]
                inputArgsDict[inputArg["name"]]={"dataType":inputArg['data_type'],"allowedValueList":allowedValsString}
            #añadimos los argumentos de salida a la acción
            for outputArg in outputArgs:
                allowedVals=outputArg['allowed_value_list']
                allowedValsString=""
                for vals in allowedVals:
                    allowedValsString+=","+vals
                allowedValsString=allowedValsString[1:len(allowedValsString)]
                outputArgsDict[outputArg["name"]]={"dataType":outputArg['data_type'],"allowedValueList":allowedValsString}
                outputArgDict={"dataType":outputArg['data_type'],"allowedValueList":allowedValsString}
                
#preparado para envio:
#guardamos en ./json/UPnP.json el json creado para hacer las pruebas de la aplicación
with open("./jsons/UPnP.json","w") as f:
    json.dump(UPnPDict, f,)
print("----------------------------------------------------------------------------\n\n")
#especificamos método de envío, url, etc
response=enviar(UPnPDict,"UPnP")
#mostramos el código de estado y la respuesta recibida
print(response.status_code)
print(response.text)



