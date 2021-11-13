import upnpy

import json
import requests
import datetime
#Método para enviar peticiones al servidor web
def enviar(j,peticion):
    jsonToSend={"Peticion":peticion, "info":j}
    jsonToSend=json.dumps(jsonToSend)
    #url="https://exploracion-iot.000webhostapp.com/controlador.php"
    url="http://localhost/ExploracionIoT/controlador.php"
    return requests.post(url, data=jsonToSend)

def consultarVulnerabilidades(nombreServicio):
    url="https://services.nvd.nist.gov/rest/json/cves/1.0/"
    #Esto sirve para añadir espacios entre las palabras
    p=""
    nombreServicio=nombreServicio.replace("_"," ").replace("-"," ")
    for l in  range(0,len(nombreServicio)):
        if(l==len(nombreServicio)):
            p=p+nombreServicio[l]
        elif(l==0):
            p=nombreServicio[l]
        elif(nombreServicio[l].isupper()):
            p=p+" "+nombreServicio[l]
        else:
            p=p+nombreServicio[l]
    pSeparados=p.split(" ")
    p=""
    for l in pSeparados:
        if(l.isupper()):
            p=p+l
        else:
            p=p+" "+l
    if(len(p)>=3):
        #Selecciono las vulnerabilidades encontradas en los últimos 3 meses en los servicios:
        fecha=datetime.datetime.now()
        fechaAhora=fecha.strftime("%Y-%m-%dT%H:%M:%S:000 UTC-00:00")
        fechaHace120dias=fecha-datetime.timedelta(days=120)
        fechaHace120dias=fechaHace120dias.strftime("%Y-%m-%dT%H:%M:%S:000 UTC-00:00")
        
        jsonVulnerabil={"keyword":p, "resultsPerPage":40,"pubStartDate": fechaHace120dias,
        "pubEndDate":fechaAhora}
        
        r=requests.get(url,params=jsonVulnerabil)
        jsonVul=r.json()
        #este if es para sí con la anterior búsqueda no ha encontrado vulnerabilidades
        if(jsonVul["totalResults"]==0):
            jsonVulnerabil={"keyword":p, "resultsPerPage":10}
            r=requests.get(url,params=jsonVulnerabil)
            return r.json()
        else:
            return r.json()
    else:
        #este else es para si no puede encontrar vulnerabilidades. En este caso, se crea un result vacío
        fecha=datetime.datetime.now()
        fechaAhora=fecha.strftime("%Y-%m-%dT%H:%M:%SZ")
        return  {"resultsPerPage": 0, "startIndex": 0, "totalResults": 0, "result": {}};

#Añadimos el UPnP al dict
DevicesDict={}
UPnPDict={"UPnP": DevicesDict} 
upnp=upnpy.UPnP()
devices=upnp.discover()
#añadimos los dispositivos al dict
for device in devices:

    #print(device.get_friendly_name())
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
        "SCPD":service.scpd_url, "ControlUrl":service.control_url, "EventUrl":service.event_sub_url, "BaseUrl":service.base_url, "actions":ActionsDict,
        "vulnerabilities":consultarVulnerabilidades(dividedService[1].replace("(","").replace(")",""))}
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



