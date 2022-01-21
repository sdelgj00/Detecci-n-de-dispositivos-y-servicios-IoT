function irPort(Port,ID){
    console.log(Port);
    //document.location.href="ScriptPuerto.php?port="+Port+" & id="+ID;
    document.location.href="ScriptPuerto.php?port="+Port+" & id="+ID;
}
function irDispositivo(IP){
    console.log(IP)
    document.location.href="Dispositivo.php?ip="+IP;
}
function irOS(ID){
    console.log(ID);
    document.location.href="ClasesOS.php?id="+ID;
}
function irUPnP(ID,IP,Port){
    console.log(ID);
    document.location.href="UPnP.php?id="+ID+" & IP="+IP+" & Port="+Port;
}
function irServUPnP(Title,ID,Prot){
    console.log(ID);
    document.location.href="ServiceUPnP.php?Title="+Title+" & id="+ID+" & Prot="+Prot;
}
function irMDNS(ID,IP,Port){
    console.log(ID);
    document.location.href="mDNS.php?id="+ID+" & IP="+IP+" & Port="+Port;
}
function irServMDNS(Title,ID,Prot){
    console.log(ID);
    document.location.href="ServiceMDNS.php?Title="+Title+" & id="+ID+" & Prot="+Prot;
}
function irWSDiscovery(ID,IP,Port){
    console.log(ID);
    document.location.href="WS-Discovery.php?id="+ID+" & IP="+IP+" & Port="+Port;
}
function irServWSDiscovery(Title,ID,Prot){
    console.log(ID);
    document.location.href="ServiceWS-Discovery.php?Title="+Title+" & id="+ID+" & Prot="+Prot;
}