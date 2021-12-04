from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from wsdiscovery import QName, Scope



from wsdiscovery.publishing import ThreadedWSPublishing as WSPublishing
    # Define type, scope & address of service
ttype1 = QName("http://www.onvif.org/ver10/device/wsdl", "Device")
scope1 = Scope("onvif://www.onvif.org/Model")
xAddr1 = "localhost:8080/abc"

    # Publish the service
wsp = WSPublishing()
wsp.start()
wsp.publishService(types=[ttype1], scopes=[scope1], xAddrs=[xAddr1])



    # Discover it (along with any other service out there)
wsd = WSDiscovery()
wsd.start()
services = wsd.searchServices()
for service in services:
    print("service: "+str(service))
    print("EPR: "+service.getEPR())
    print("InstanceId: "+str(service.getInstanceId()))
    print("MessageNumber: "+str(service.getMessageNumber()))
    print("MetadataVersion: "+str(service.getMetadataVersion()))
    print("Scopes: "+str(service.getScopes()))#list
    for scope in service.getScopes():
        print("---scope MatchBy :"+scope.getMatchBy())
        print("---scope QuotedValue :"+scope.getQuotedValue())
        print("---scope Value :"+scope.getValue())
    print("Types: "+str(service.getTypes()))#list
    for type in service.getTypes():
        print("---type:"+str(type))
    print("XAddrs: "+str(service.getXAddrs()))
    print("----------------------------------")
wsd.stop()

















