ExploradorIoT=(" _____            _                     _              ___    _____\n"
"| ____|_  ___ __ | | ___  _ __ __ _  __| | ___  _ __  |_ _|__|_   _|\n"
"|  _| \ \/ / '_ \| |/ _ \| '__/ _` |/ _` |/ _ \| '__|  | |/ _ \| |\n"
"| |___ >  <| |_) | | (_) | | | (_| | (_| | (_) | |     | | (_) | |\n"
"|_____/_/\_\ .__/|_|\___/|_|  \__,_|\__,_|\___/|_|    |___\___/|_|\n"
"           |_|\n")
Autor="Saul Delgado Jimeno"
nmap="\nNmap:\n"
mdns="\nmDNS:\n"
upnp="\nUPnP:\n"
wsdiscovery="\nWS-Discovery:\n"

def tituloExploracion(valor):
    if valor=="nmap":
        return nmap
    elif valor=="mdns":
        return mdns
    elif valor=="upnp":
        return upnp
    elif valor=="wsdiscovery":
        return wsdiscovery