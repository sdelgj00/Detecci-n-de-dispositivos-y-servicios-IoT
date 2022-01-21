<?php
require("constantes.php");
class accesoSql {
    private $conexion;
    
    private function compVacio($vac){
        $xtra=strval($vac);
        if($xtra==''){
            return 0;
        }else{
            return $vac;
        }
    }

    function sql($sql) {

        // Comprobamos que no hemos abierto ya la conexión
        if (!$this->conexion)  {
            //Abrimos conexión con la base de datos. Los valores están definidos en config.php
            $this->conexion = @new mysqli(
                constant("DB_HOST"), constant("DB_USER"), constant("DB_PASSWORD"), constant("DB_NAME"));

            // Comprobamos si hay algún error de conexión
            if ($this->conexion->connect_errno) {
                printf("Error: %s\n", $this->conexion->connect_error);   die();
            }
        }

        //Ejecutamos el SQL
        $res=$this->conexion->query($sql);
        if(is_bool($res)){
            return $res;
        }
        else if ($res) {
            // Esta función devuelve todas las filas en formato array de PHP.
            return (array)$res->fetch_all(MYSQLI_ASSOC);
        }
        else {
            return false;
        }
    }
	
    function anyadirInfoDispositivo($ip,$atr){
        $salida="";
        $salida.=$ip."\n";

        //Esta linea es para poner todos los dispositivos como no accesibles
        
        $uptime=0;
        if($atr["uptime"]["seconds"]){
            $uptime=$atr["uptime"]["seconds"];
        }
        //Si no existe el dispositivo, lo creamos
	    //Si existe, lo actualizamos
        if($this->existeDispositivo($ip)){
            $salida.="existe ".$ip."\n";
            $consulta="UPDATE dispositivo SET IP='".$ip."', HostName='".$atr["hostnames"][0]["name"]."', Type='".$atr["hostnames"][0]["type"]."', Mac='".$atr["addresses"]["mac"]."', Vendor='".$atr["vendor"][$atr["addresses"]["mac"]]."', Uptime='".$uptime."', State='up' WHERE IP = '".$ip."'";
	        $res=$this->sql($consulta);
	        $salida.=$consulta."\n";
            $salida.="existe ".$ip."\n";
        }else{
            $salida.="no existe ".$ip."\n";
            $consulta="INSERT INTO dispositivo(IP, HostName, Type, Mac, Vendor, Uptime, State) VALUES ('".$ip."', '".$atr["hostnames"][0]["name"]."','".$atr["hostnames"][0]["type"]."','".$atr["addresses"]["mac"]."','".$atr["vendor"][$atr["addresses"]["mac"]]."','".$uptime."','up')";
            $res=$this->sql($consulta);
            $salida.=$consulta;
            $salida.="creado\n";
        }
        $salida.=$this->anyadirPort($ip,$atr);
        $salida.=$this->anyadirHostScript($ip,$atr);
        $salida.=$this->anyadirOsScript($ip,$atr);
        return $salida;
    }

    function anyadirOsScript($ip,$atr){
        $salida="";
        $res=$this->sql("DELETE FROM os_script WHERE IP = '".$ip."'");
        $salida.="Borrado contenido os script\n";
        foreach ($atr["osmatch"] as $k => $v){
            $consulta="INSERT INTO os_script(IP,Name,Accuracy,Line) values ('".$ip."',
            '".$v["name"]."','".$v["accuracy"]."','".$v["line"]."')";
            $res=$this->sql($consulta);
            $datosOsScript=$this->sql("SELECT * FROM os_script WHERE IP='".$ip."' AND Name= '".$v["name"]."' AND Accuracy= '".$v["accuracy"]."'");
            $salida.=$consulta."\n";
            foreach ($v["osclass"] as $k2 => $v2){
                $res2=$this->sql("INSERT INTO os_class(ID_os_script,Type,Vendor,Osfamily,Osgen,Accuracy,Cpe) values (  
                '".$datosOsScript[0]["ID"]."','".$v2["type"]."','".$v2["vendor"]."','".$v2["osfamily"]."','".$v2["osgen"]."',
                '".$v2["accuracy"]."','".$v2["cpe"][0]."')");
            }
        }
        return $salida;
    }

    function anyadirHostScript($ip,$atr){
        $salida="";
        $res=$this->sql("DELETE FROM host_script WHERE IP = '".$ip."'");
        $salida.="Borrado contenido host script\n";
        foreach ($atr["hostscript"] as $k => $v){
            $consulta="INSERT INTO host_script(IP,Llave,Valor) values ('".$ip."',
            '".$v["id"]."','".$v["output"]."')";
            $res=$this->sql($consulta);
            $salida.=$consulta."\n";
        }
        return $salida;
    }
    function anyadirPort($ip,$atr){
        $salida="";
        $res=$this->sql("DELETE FROM port WHERE IP = '".$ip."'");
        $salida.="Borrado contenido\n";
        $listaPuertos=array();
        if($atr["tcp"]){
            foreach ($atr["tcp"] as $port => $i){
                array_push($listaPuertos,$port,"");
                $salida.="puerto ".$port."\n";
                $consulta="INSERT INTO port(IP,Port,Type,State,Name,Product,Version, ExtraInfor,Conf,Cpe)
                values ('".$ip."','".$port."','tcp','".$i["state"]."','".$i["name"]."','".$i["product"]."','".$i["version"]."',
                '".$i["extrainfo"]."','".$i["conf"]."','".$i["cpe"]."')";
                $res2=$this->sql($consulta);
                $salida.=$consulta."\n";
                $datosPort=$this->sql("SELECT * FROM port WHERE IP='".$ip."'AND Port='".$port."'");
                foreach($i["script"] as $k => $v){
                    $consulta2="INSERT INTO port_script(ID_Port,Llave,Valor) values 
                    ('".$datosPort[0]["ID"]."','".$k."','".$v."')";
                    $salida.="\n".$consulta2."\n";
                    $res3=$this->sql($consulta2);
                }
            }
        }
        if($atr["udp"]){
            foreach ($atr["udp"] as $port => $i){
                array_push($listaPuertos,$port,"");
                $salida.="puerto ".$port."\n";                
                $res2=$this->sql("INSERT INTO port(IP,Port,Type,State,Name,Product,Version, ExtraInfor,Conf,Cpe)
                values ('".$ip."','".$port."','udp','".$i["state"]."','".$i["name"]."','".$i["product"]."','".$i["version"]."',
                '".$i["extrainfo"]."','".$i["conf"]."','".$i["cpe"]."')");
                $datosPort=$this->sql("SELECT * FROM port WHERE IP='".$ip."'AND Port='".$port."'");                
                foreach($i["script"] as $k => $v){
                    $res3=$this->sql("INSERT INTO port_script(ID_Port,Llave,Valor) values 
                    ('".$datosPort[0]["ID"]."','".$k."','".$v."')");
                }
            }
        }

        if($atr["portused"]){
            foreach ($atr["portused"] as $num => $i){
                $salida.="cucu\n";
                $salida.=$i["portid"];
                foreach($listaPuertos as $a =>$b){
                    $salida.=$b."\n";
                }
                if(!in_array($i["portid"],$listaPuertos)){
                    array_push($listaPuertos,$i["portid"],"");
                    $res2=$this->sql("INSERT INTO port(IP, Port, Type, State) values
                    ('".$ip."','".$i["portid"]."','".$i["proto"]."','".$i["state"]."')");
                }
            }
        }
        return $salida;
    }

    function anyadirBase($a,$clave){
        $salida="";
	    if($clave=="Nmap"){
	    	$salida=$salida."Hay Nmap\n";
	    	echo "holas\n".$a;
	    	echo "\n".$a["Nmap"];
	    	$resUpToDown=$this->sql("UPDATE dispositivo SET State='down'");
            foreach ($a["Nmap"] as $ip => $atr){
                $salida.=$this->anyadirInfoDispositivo($ip, $atr);
                //Obtenemos el ID de la app añadida/modificada en el anyadirApp()
               /* $salida.=$idApp[0]["IP"]." ".$idApp[0]["Port"];
                $salida.=$this->anyadirAppUPnP($idApp[0]["ID"],$atr);

                //Obtenemos el ID de la app añadida/modificada en el anyadirAppUPnP()
                $idAppUPnP = $this->sql("SELECT * FROM app_UPnP WHERE ID_APP = '".$idApp[0]["ID"]."'");
                $salida.=$this->anyadirServiciosUPnP($idAppUPnP[0]["ID"],$atr["services"]);*/


            }
	    }
        if($clave=="UPnP"){
            $salida=$salida."Hay UPnP\n";
            foreach ($a["UPnP"] as $ipPuerto => $atr){
                $partesIPPuerto=explode(":",$ipPuerto);
                $ip=$partesIPPuerto[0];
                $port=$partesIPPuerto[1];
                $salida.=$this->anyadirBaseDispositivo($ip);
                $salida.=$this->anyadirApp($ip,$port);
                //Obtenemos el ID de la app añadida/modificada en el anyadirApp()
                $idApp = $this->sql("SELECT * FROM app WHERE IP = '".$ip."' AND Port = '".$port."'");
                $salida.="check1";
                $salida.=$idApp[0]["IP"]." ".$idApp[0]["Port"];
                $salida.=$this->anyadirAppUPnP($idApp[0]["ID"],$atr);

                //Obtenemos el ID de la app añadida/modificada en el anyadirAppUPnP()
                $idAppUPnP = $this->sql("SELECT * FROM app_UPnP WHERE ID_APP = '".$idApp[0]["ID"]."'");
                $salida.=$this->anyadirServiciosUPnP($idAppUPnP[0]["ID"],$atr["services"]);


            }
        }
        if($clave=="mDNS"){
            $salida=$salida."hay mDNS\n";
            foreach ($a["mDNS"] as $ipPuerto => $atr){
                $partesIPPuerto=explode(":",$ipPuerto);
                $ip=$partesIPPuerto[0];
                $port=$partesIPPuerto[1];
                $salida.=$this->anyadirBaseDispositivo($ip);
                $salida.=$this->anyadirApp($ip,$port);
                //Obtenemos el ID de la app añadida/modificada en el anyadirApp()
                $idApp = $this->sql("SELECT * FROM app WHERE IP = '".$ip."' AND Port = '".$port."'");
                $salida.=$this->anyadirAppmDNS($idApp[0]["ID"],$atr);

                //Obtenemos el ID de la app añadida/modificada en el anyadirAppUPnP()
                $idAppmDNS = $this->sql("SELECT * FROM app_mDNS WHERE ID_APP = '".$idApp[0]["ID"]."'");
                $salida.=$this->anyadirServiciosmDNS($idAppmDNS[0]["ID"],$atr);
            }
        }
        if($clave=="WS-Discovery"){
            $salida=$salida."hay WS-Discovery\n";
            foreach ($a["WS-Discovery"] as $ipPuerto => $atr){
                $partesIPPuerto=explode(":",$ipPuerto);
                $ip=$partesIPPuerto[0];
                $port=$partesIPPuerto[1];
                $salida.=$this->anyadirBaseDispositivo($ip);
                $salida.=$this->anyadirApp($ip,$port);
                //Obtenemos el ID de la app añadida/modificada en el anyadirApp()
                $idApp = $this->sql("SELECT * FROM app WHERE IP = '".$ip."' AND Port = '".$port."'");
                $salida.=$this->anyadirAppWSDiscovery($idApp[0]["ID"],$atr);

                //Obtenemos el ID de la app añadida/modificada en el anyadirAppUPnP()
                $idAppWSDiscovery = $this->sql("SELECT * FROM app_WSDiscovery WHERE ID_APP = '".$idApp[0]["ID"]."'");
                $salida.=$this->anyadirServiciosWSDiscovery($idAppWSDiscovery[0]["ID"],$atr);
            }
        }
        return $salida;
    }

    function anyadirAppWSDiscovery($idApp, $atr){
        $salida="";
        $res=$this->sql("SELECT * FROM app_WSDiscovery WHERE ID_APP = '".$idApp."' ");
        if(count($res)>0){
            $salida.="existe WSDiscovery ".$idApp."\n";
        }else{
            $salida.="no existe WSDiscovery ".$idApp."\n";
            $res2=$this->sql("INSERT INTO app_WSDiscovery(ID_APP) values ('".$idApp."')");
        }
        return $salida;
    }

    function anyadirServiciosWSDiscovery($idAppWSDiscovery, $atr){
        $salida="";
        foreach ($atr as $serviceName => $serviceAtr) {
            $res=$this->sql("SELECT * FROM service_WSDiscovery WHERE ID_APP_WSDiscovery = '".$idAppWSDiscovery."' AND XAddrs = '".$serviceName."'");
            if(count($res)>0){
                $salida.="SERVICIO WSDiscovery ".$serviceName." ya añadido\n";
                $consulta2="UPDATE service_WSDiscovery SET EPR = '".$serviceAtr["EPR"]."', InstanceId  = '".$serviceAtr["InstanceId"]."',
                MessageNumber = '".$serviceAtr["MessageNumber"]."', MetadataVersion = '".$serviceAtr["MetadataVersion"]."', XAddrs = '".$serviceAtr["XAddrs"]."'
                WHERE ID_APP_WSDiscovery = '".$idAppWSDiscovery."' AND XAddrs= '".$serviceName."'";
                $salida.=$consulta2;
                $res2=$this->sql($consulta2);
            }else{
                $salida.= "SERVICIO WSDiscovery ".$serviceName." no añadido\n";
                $consulta2="INSERT INTO service_WSDiscovery (ID_APP_WSDiscovery, EPR, InstanceId, MessageNumber, MetadataVersion, XAddrs) values
                (".$idAppWSDiscovery.",'".$serviceAtr["EPR"]."','".$serviceAtr["InstanceId"]."','".$serviceAtr["MessageNumber"]."',
                '".$serviceAtr["MetadataVersion"]."','".$serviceAtr["XAddrs"]."')";
                $salida.=$consulta2;
                $res2=$this->sql($consulta2);

            }
            $idServicio=$this->sql("SELECT * FROM service_WSDiscovery WHERE ID_APP_WSDiscovery = '".$idAppWSDiscovery."' AND XAddrs= '".$serviceName."'");
            $salida.=$this->anyadirScopesWSDiscovery($idServicio[0]["ID"],$serviceAtr["Scopes"]);
            $salida.=$this->anyadirTypesWSDiscovery($idServicio[0]["ID"],$serviceAtr["Types"]);
            $salida.=$this->anyadirVulnerabilidadesWSDiscovery($idServicio[0]["ID"],$serviceAtr["vulnerabilities"]);
        }
        return $salida;
    }

    function anyadirScopesWSDiscovery($idServicioWSDiscovery, $scopes){
        $salida="";
        $resDel=$this->sql("DELETE FROM scope_WSDiscovery WHERE ID_SERVICE = '".$idServicioWSDiscovery."'");
        foreach ($scopes as $scopeKey => $scopeValue){
            $salida.="Scope WSDiscovery ".$scopeKey."\n";
            $res=$this->sql("INSERT INTO scope_WSDiscovery(ID_SERVICE, MatchBy, QuotedValue, Value) values ('".$idServicioWSDiscovery."','".$scopeValue["MatchBy"]."', '".$scopeValue["QuotedValue"]."', '".$scopeValue["Value"]."')");
        }
        return $salida;
    }

    function anyadirTypesWSDiscovery($idServicioWSDiscovery, $types){
        $salida="";
        $resDel=$this->sql("DELETE FROM type_WSDiscovery WHERE ID_SERVICE = '".$idServicioWSDiscovery."'");
        foreach ($types as $typeKey => $typeValue){
            $salida.="Type WSDiscovery ".$typeKey."\n";
            $res=$this->sql("INSERT INTO type_WSDiscovery(ID_SERVICE, TypeName) values ('".$idServicioWSDiscovery."','".$typeValue."')");
        }
        return $salida;
    }
    function anyadirVulnerabilidadesWSDiscovery($idServicio, $vulnerabilities){
        $salida="";
        if($vulnerabilities["resultsPerPage"]==0) {
            $salida .= "No hay vulnerabilidades WS-Discovery\n";
            $res = $this->sql("DELETE FROM vulnerability_WSDiscovery WHERE ID_SERVICE= '" . $idServicio . "'");
        }else{
            $salida.="hay ".$vulnerabilities["resultsPerPage"]." vulnerabilidades\n";
            $res=$this->sql("DELETE FROM vulnerability_WSDiscovery WHERE ID_SERVICE= '".$idServicio."'");
            foreach($vulnerabilities["result"]["CVE_Items"] as $number => $vul){
                $salida.="vulnerabilidad ".$number."\n";
                $impactv2=$vul["impact"]["baseMetricV2"];
                $impactv3=$vul["impact"]["baseMetricV3"];
                $consulta="INSERT INTO vulnerability_WSDiscovery (ID_SERVICE, PublishDate, LastModifiedDate, Description, Lang,bmv2severity,bmv2explitabilityScore,
	            bmv2impactScore,bmv2acInsufInfo,bmv2obtainAllPrivilege,	bmv2obtainUserPrivilege,bmv2obtainOtherPrivilege,bmv2userInteractionRequired,bmv2accessVector,
                bmv2accessComplexity,bmv2authentication,bmv2confidentialityImpact,bmv2integrityImpact,bmv2availabilityImpact,bmv2baseScore,
                bmv3exploitabilityScore,bmv3impactScore,bmv3attackVector,bmv3attackComplexity,bmv3privilegesRequired,bmv3userInteraction,bmv3scope,bmv3confidentialImpact,
                bmv3integrityImpact,bmv3availabilityImpact,bmv3baseScore,bmv3baseSeverity) values
                ('".$idServicio."','".str_replace("Z","",str_replace("T",":",$vul["publishedDate"]))."','".str_replace("Z","",str_replace("T",":",$vul["lastModifiedDate"]))."','".str_replace("'","`",$vul["cve"]["description"]["description_data"][0]["value"])."',
                '".$vul["cve"]["description"]["description_data"][0]["lang"]."','".$impactv2["severity"]."','".$this->compVacio($impactv2["exploitabilityScore"])."',
                '".$this->compVacio($impactv2["impactScore"])."',b'".$impactv2["acInsufInfo"]."',b'".$impactv2["obtainAllPrivilege"]."',b'".$impactv2["obtainUserPrivilege"]."',b'".$impactv2["obtainOtherPrivilege"]."',b'".$impactv2["userInteractionRequired"]."',
                '".$impactv2["cvssV2"]["accessVector"]."','".$impactv2["cvssV2"]["accessComplexity"]."','".$impactv2["cvssV2"]["authentication"]."','".$impactv2["cvssV2"]["confidentialityImpact"]."',
                '".$impactv2["cvssV2"]["integrityImpact"]."','".$impactv2["cvssV2"]["availabilityImpact"]."','".$this->compVacio($impactv2["cvssV2"]["baseScore"])."',
                '".$this->compVacio($impactv3["exploitabilityScore"])."','".$this->compVacio($impactv3["impactScore"])."','".$impactv3["cvssV3"]["attackVector"]."','".$impactv3["cvssV3"]["attackComplexity"]."',
                '".$impactv3["cvssV3"]["privilegesRequired"]."','".$impactv3["cvssV3"]["userInteraction"]."','".$impactv3["cvssV3"]["scope"]."','".$impactv3["cvssV3"]["confidentialityImpact"]."',
                '".$impactv3["cvssV3"]["integrityImpact"]."','".$impactv3["cvssV3"]["availabilityImpact"]."','".$this->compVacio($impactv3["cvssV3"]["baseScore"])."','".$impactv3["cvssV3"]["baseSeverity"]."')";
                $res2=$this->sql($consulta);
                $salida.=$res2."\n";
                //este if es por si hay algún fallo en la consulta
                if($res2==""){
                    $salida.=$consulta."\n";
                }
            }
        }
        return $salida;
    }
    function anyadirAppmDNS($idApp, $atr){
        $salida="";
        $res=$this->sql("SELECT * FROM app_mDNS WHERE ID_APP = '".$idApp."' ");
        if(count($res)>0){
            $salida.="existe mDNS ".$idApp."\n";
        }else{
            $salida.="no existe mDNS ".$idApp."\n";
            $res2=$this->sql("INSERT INTO app_mDNS(ID_APP) values ('".$idApp."')");
        }
        return $salida;
    }

    function anyadirServiciosmDNS($idAppmDNS, $atr)
    {
        $salida="";
        foreach ($atr as $serviceName => $serviceAtr) {
            $res=$this->sql("SELECT * FROM service_mDNS WHERE ID_APP_MDNS = '".$idAppmDNS."' AND Name= '".$serviceName."'");
            if(count($res)>0){
                $salida.="SERVICIO mDNS".$serviceName." ya añadido\n";
                $consulta2="UPDATE service_mDNS SET Type = '".$serviceAtr["type"]."', Weight = '".$this->compVacio($serviceAtr["weight"])."',
                Priority = '".$this->compVacio($serviceAtr["priority"])."', Server = '".$serviceAtr["server"]."', InterfaceIndex = '".$this->compVacio($serviceAtr["interface_index"])."'
                WHERE ID_APP_MDNS = '".$idAppmDNS."' AND Name= '".$serviceName."'";
                $salida.=$consulta2;
                $res2=$this->sql($consulta2);
                $salida.=$this->compVacio($serviceAtr["interface_index"]);
            }else{
                $salida.= "SERVICIO mDNS".$serviceName." no añadido\n";
                $consulta2="INSERT INTO service_mDNS (ID_APP_MDNS, Name, Type, Weight, Priority, Server, InterfaceIndex) values
                (".$idAppmDNS.",'".$serviceName."','".$serviceAtr["type"]."','".$this->compVacio($serviceAtr["weight"])."','".$this->compVacio($serviceAtr["priority"])."',
                '".$serviceAtr["server"]."','".$this->compVacio($serviceAtr["interface_index"])."')";
                $salida.=$consulta2;
                $salida.=$this->compVacio($serviceAtr["interface_index"]);
                $res2=$this->sql($consulta2);

            }
            $idServicio=$this->sql("SELECT * FROM service_mDNS WHERE ID_APP_MDNS = '".$idAppmDNS."' AND Name= '".$serviceName."'");
            $salida.=$this->anyadirPropertiesmDNS($idServicio[0]["ID"],$serviceAtr["properties"]);
            $salida.=$this->anyadirVulnerabilidadesmDNS($idServicio[0]["ID"],$serviceAtr["vulnerabilities"]);
        }
        return $salida;
    }
    function anyadirPropertiesmDNS($idServiciomDNS, $properties){
        $salida="";
        $resDel=$this->sql("DELETE FROM property_mDNS WHERE ID_SERVICE_MDNS = '".$idServiciomDNS."'");
        //$res=$this->sql("INSERT INTO property_mDNS(ID_SERVICE_MDNS, Llave, Valor) values ('".$idServiciomDNS."','hola', 'adios')");
        foreach ($properties as $propertyKey => $propertyValue){
            $salida.="Property mDNS ".$propertyKey."\n";
            $res=$this->sql("INSERT INTO property_mDNS(ID_SERVICE_MDNS, Llave, Valor) values ('".$idServiciomDNS."','".$propertyKey."', '".$propertyValue."')");
        }
        return $salida;
    }
    function anyadirVulnerabilidadesmDNS($idServicio, $vulnerabilities){
        $salida="";
        if($vulnerabilities["resultsPerPage"]==0) {
            $salida .= "No hay vulnerabilidades mDNS\n";
            $res = $this->sql("DELETE FROM vulnerability_mDNS WHERE ID_SERVICE= '" . $idServicio . "'");
        }else{
            $salida.="hay ".$vulnerabilities["resultsPerPage"]." vulnerabilidades\n";
            $res=$this->sql("DELETE FROM vulnerability_mDNS WHERE ID_SERVICE= '".$idServicio."'");
            foreach($vulnerabilities["result"]["CVE_Items"] as $number => $vul){
                $salida.="vulnerabilidad ".$number."\n";
                $impactv2=$vul["impact"]["baseMetricV2"];
                $impactv3=$vul["impact"]["baseMetricV3"];
                $consulta="INSERT INTO vulnerability_mDNS (ID_SERVICE, PublishDate, LastModifiedDate, Description, Lang,bmv2severity,bmv2explitabilityScore,
	            bmv2impactScore,bmv2acInsufInfo,bmv2obtainAllPrivilege,	bmv2obtainUserPrivilege,bmv2obtainOtherPrivilege,bmv2userInteractionRequired,bmv2accessVector,
                bmv2accessComplexity,bmv2authentication,bmv2confidentialityImpact,bmv2integrityImpact,bmv2availabilityImpact,bmv2baseScore,
                bmv3exploitabilityScore,bmv3impactScore,bmv3attackVector,bmv3attackComplexity,bmv3privilegesRequired,bmv3userInteraction,bmv3scope,bmv3confidentialImpact,
                bmv3integrityImpact,bmv3availabilityImpact,bmv3baseScore,bmv3baseSeverity) values
                ('".$idServicio."','".str_replace("Z","",str_replace("T",":",$vul["publishedDate"]))."','".str_replace("Z","",str_replace("T",":",$vul["lastModifiedDate"]))."','".str_replace("'","`",$vul["cve"]["description"]["description_data"][0]["value"])."',
                '".$vul["cve"]["description"]["description_data"][0]["lang"]."','".$impactv2["severity"]."','".$this->compVacio($impactv2["exploitabilityScore"])."',
                '".$this->compVacio($impactv2["impactScore"])."',b'".$impactv2["acInsufInfo"]."',b'".$impactv2["obtainAllPrivilege"]."',b'".$impactv2["obtainUserPrivilege"]."',b'".$impactv2["obtainOtherPrivilege"]."',b'".$impactv2["userInteractionRequired"]."',
                '".$impactv2["cvssV2"]["accessVector"]."','".$impactv2["cvssV2"]["accessComplexity"]."','".$impactv2["cvssV2"]["authentication"]."','".$impactv2["cvssV2"]["confidentialityImpact"]."',
                '".$impactv2["cvssV2"]["integrityImpact"]."','".$impactv2["cvssV2"]["availabilityImpact"]."','".$this->compVacio($impactv2["cvssV2"]["baseScore"])."',
                '".$this->compVacio($impactv3["exploitabilityScore"])."','".$this->compVacio($impactv3["impactScore"])."','".$impactv3["cvssV3"]["attackVector"]."','".$impactv3["cvssV3"]["attackComplexity"]."',
                '".$impactv3["cvssV3"]["privilegesRequired"]."','".$impactv3["cvssV3"]["userInteraction"]."','".$impactv3["cvssV3"]["scope"]."','".$impactv3["cvssV3"]["confidentialityImpact"]."',
                '".$impactv3["cvssV3"]["integrityImpact"]."','".$impactv3["cvssV3"]["availabilityImpact"]."','".$this->compVacio($impactv3["cvssV3"]["baseScore"])."','".$impactv3["cvssV3"]["baseSeverity"]."')";
                $res2=$this->sql($consulta);
                $salida.=$res2."\n";
                //este if es por si hay algún fallo en la consulta
                if($res2==""){
                    $salida.=$consulta."\n";
                }
            }
        }
        return $salida;
    }
    function anyadirServiciosUPnP($idAppUPnP, $atr)
    {
        $salida="";
        foreach ($atr as $serviceName => $serviceAtr) {
            $res=$this->sql("SELECT * FROM service_UPnP WHERE ID_APP = '".$idAppUPnP."' AND Name= '".$serviceName."'");
            if(count($res)>0){
                $salida.="SERVICIO UPnP".$serviceName." ya añadido\n";
                $res2=$this->sql("UPDATE service_UPnP SET ID_Name= '".$serviceAtr["ID"]."', SCPD= '".$serviceAtr["SCPD"]."', 
                ControlUrl= '".$serviceAtr["ControlUrl"]."', EventUrl= '".$serviceAtr["EventUrl"]."', BaseUrl= '".$serviceAtr["BaseUrl"]."' 
                WHERE ID_APP = '".$idAppUPnP."' AND Name= '".$serviceName."'");
            }else{
                $salida.= "SERVICIO UPnP".$serviceName." no añadido\n";
                $res2=$this->sql("INSERT INTO service_UPnP (Name, ID_Name, SCPD, ControlUrl, EventUrl, BaseUrl, ID_APP) values
                ('".$serviceName."','".$serviceAtr["ID"]."','".$serviceAtr["SCPD"]."','".$serviceAtr["ControlUrl"]."','".$serviceAtr["EventUrl"]."',
                '".$serviceAtr["BaseUrl"]."','".$idAppUPnP."')");
            }
            $idServicio=$this->sql("SELECT * FROM service_UPnP WHERE ID_APP = '".$idAppUPnP."' AND Name= '".$serviceName."'");
            $salida.=$this->anyadirActionsUPnP($idServicio[0]["ID"],$serviceAtr["actions"]);
            $salida.=$this->anyadirVulnerabilidadesUPnP($idServicio[0]["ID"],$serviceAtr["vulnerabilities"]);
        }
        return $salida;
    }
    function anyadirActionsUPnP($idServicio, $actions){
        $salida="";
        $resDel=$this->sql("DELETE FROM action_UPnP WHERE ID_SERVICE= '".$idServicio."'");
        foreach ($actions as $actionName => $actionAtrr){
            $res=$this->sql("INSERT INTO action_UPnP(Name, ID_SERVICE) values ('".$actionName."','".$idServicio."')");
            $salida.="UPnP action ".$actionName."\n";
            $resIdAction=$this->sql("SELECT * FROM action_UPnP WHERE ID_SERVICE = '".$idServicio."' AND Name = '".$actionName."'");
            foreach ($actionAtrr["input_args"] as $argName => $argAtrr){
                $salida.="UPnP inputArg ".$argName."\n";
                $res2=$this->sql("INSERT INTO input_arg_UPnP(ID_ACTION, Name, DataType, AllowedValueList) values ('".$resIdAction[0]["ID"]."',
                '".$argName."','".$argAtrr["dataType"]."','".$argAtrr["allowedValueList"]."')");
            }
            foreach ($actionAtrr["output_args"] as $argName => $argAtrr){
                $salida.="UPnP outputArg ".$argName."\n";
                $res3=$this->sql("INSERT INTO output_arg_UPnP(ID_ACTION, Name, DataType, AllowedValueList) values ('".$resIdAction[0]["ID"]."',
                '".$argName."','".$argAtrr["dataType"]."','".$argAtrr["allowedValueList"]."')");
            }
        }
        return $salida;
    }
    function anyadirVulnerabilidadesUPnP($idServicio, $vulnerabilities){
        $salida="";
        if($vulnerabilities["resultsPerPage"]==0) {
            $salida .= "No hay vulnerabilidades UPnP\n";
            $res = $this->sql("DELETE FROM vulnerability_UPnP WHERE ID_SERVICE= '" . $idServicio . "'");
        }else{
            $salida.="hay ".$vulnerabilities["resultsPerPage"]." vulnerabilidades\n";
            $res=$this->sql("DELETE FROM vulnerability_UPnP WHERE ID_SERVICE= '".$idServicio."'");
            foreach($vulnerabilities["result"]["CVE_Items"] as $number => $vul){
                $salida.="vulnerabilidad ".$number."\n";
                $impactv2=$vul["impact"]["baseMetricV2"];
                $impactv3=$vul["impact"]["baseMetricV3"];
                $consulta="INSERT INTO vulnerability_UPnP (ID_SERVICE, PublishDate, LastModifiedDate, Description, Lang,bmv2severity,bmv2explitabilityScore,
	            bmv2impactScore,bmv2acInsufInfo,bmv2obtainAllPrivilege,	bmv2obtainUserPrivilege,bmv2obtainOtherPrivilege,bmv2userInteractionRequired,bmv2accessVector,
                bmv2accessComplexity,bmv2authentication,bmv2confidentialityImpact,bmv2integrityImpact,bmv2availabilityImpact,bmv2baseScore,
                bmv3exploitabilityScore,bmv3impactScore,bmv3attackVector,bmv3attackComplexity,bmv3privilegesRequired,bmv3userInteraction,bmv3scope,bmv3confidentialImpact,
                bmv3integrityImpact,bmv3availabilityImpact,bmv3baseScore,bmv3baseSeverity) values
                ('".$idServicio."','".str_replace("Z","",str_replace("T",":",$vul["publishedDate"]))."','".str_replace("Z","",str_replace("T",":",$vul["lastModifiedDate"]))."','".str_replace("'","`",$vul["cve"]["description"]["description_data"][0]["value"])."',
                '".$vul["cve"]["description"]["description_data"][0]["lang"]."','".$impactv2["severity"]."','".$this->compVacio($impactv2["exploitabilityScore"])."',
                '".$this->compVacio($impactv2["impactScore"])."',b'".$impactv2["acInsufInfo"]."',b'".$impactv2["obtainAllPrivilege"]."',b'".$impactv2["obtainUserPrivilege"]."',b'".$impactv2["obtainOtherPrivilege"]."',b'".$impactv2["userInteractionRequired"]."',
                '".$impactv2["cvssV2"]["accessVector"]."','".$impactv2["cvssV2"]["accessComplexity"]."','".$impactv2["cvssV2"]["authentication"]."','".$impactv2["cvssV2"]["confidentialityImpact"]."',
                '".$impactv2["cvssV2"]["integrityImpact"]."','".$impactv2["cvssV2"]["availabilityImpact"]."','".$this->compVacio($impactv2["cvssV2"]["baseScore"])."',
                '".$this->compVacio($impactv3["exploitabilityScore"])."','".$this->compVacio($impactv3["impactScore"])."','".$impactv3["cvssV3"]["attackVector"]."','".$impactv3["cvssV3"]["attackComplexity"]."',
                '".$impactv3["cvssV3"]["privilegesRequired"]."','".$impactv3["cvssV3"]["userInteraction"]."','".$impactv3["cvssV3"]["scope"]."','".$impactv3["cvssV3"]["confidentialityImpact"]."',
                '".$impactv3["cvssV3"]["integrityImpact"]."','".$impactv3["cvssV3"]["availabilityImpact"]."','".$this->compVacio($impactv3["cvssV3"]["baseScore"])."','".$impactv3["cvssV3"]["baseSeverity"]."')";
                $res2=$this->sql($consulta);
                $salida.=$res2."\n";
                //este if es por si hay algún fallo en la consulta
                if($res2==""){
                    $salida.=$consulta."\n";
                }
            }
        }
        return $salida;
    }
    function anyadirApp($ip,$port){
        $salida="";
        $res=$this->sql("SELECT * FROM app WHERE IP = '".$ip."' AND Port = '".$port."'");
        if(count($res)>0){
            $salida.="existe ".$ip." ".$port."\n";
        }else{
            $salida.="no existe ".$ip." ".$port."\n";
            $res2=$this->sql("INSERT INTO app(IP,Port) values ('".$ip."','".$port."')");
        }
        return $salida;
    }
    //comprobamos que no se ha añadido previamente la AppUPnP, si no la anyadimos o la actualizamos
    function anyadirAppUPnP($idApp,$atr){
        $salida="";
        $res=$this->sql("SELECT * FROM app_UPnP WHERE ID_APP = '".$idApp."' ");
        if(count($res)>0){
            $salida.="existe UPnP ".$idApp." ".$atr['port']."\n";
            $res2=$this->sql("UPDATE app_UPnP SET Name = '".$atr["Name"]."' WHERE ID = '".$res[0]["ID"]."'");
        }else{
            $salida.="no existe UPnP ".$idApp." ".$atr['port']."\n";
            $res2=$this->sql("INSERT INTO app_UPnP(ID_APP,Name) values ('".$idApp."','".$atr["Name"]."')");
        }
        return $salida;
    }
    //Comprobamos que el dispositivo está en la base, y si no lo esta, lo anyadimos
    function anyadirBaseDispositivo($ip){
        $salida="";
        $salida.=$ip."\n";
        //Si no existe el dispositivo, lo creamos
        if($this->existeDispositivo($ip)){
            $salida.="existe ".$ip."\n";
        }else{
            $salida.="no existe ".$ip."\n";
            $this->crearDispositivo($ip);
            $salida.="creado\n";
        }
        return $salida;
    }
    //Devuelve si existe el dispositivo
    function existeDispositivo($ip){
        $res=$this->sql("SELECT * FROM dispositivo WHERE IP= '".$ip."'");
        if(count($res)>0){
            return true;
        }else{
            return false;
        }

    }
    //Anyade el dispositivo que recibe a la base de datos
    function crearDispositivo($ip){
        $res=$this->sql("INSERT INTO dispositivo(IP, State) VALUES ('".$ip."', 'up')");
    }
    




    function mostrarApps(){
        $res=$this->sql("SELECT * FROM app");
        $salida="<table><tr>
                <th>Nº</th>
                <th>IP</th>
                <th>PORT</th>
                <th>PROTOCOL</th>

            </tr>";
        $contador=1;
        foreach($res as $value){
            $salida.="<tr><td><button onclick=dispositivo('".$value["ID"]."')>".$contador."</button></td>";
            $salida.="<td>".$value["IP"]."</td><td>".$value["Port"]."</td>";
            $resUPnP=$this->sql("SELECT * FROM app_UPnP WHERE ID_APP = '".$value["ID"]."'");
            $resmDNS=$this->sql("SELECT * FROM app_mDNS WHERE ID_APP = '".$value["ID"]."'");
            $resWSDiscovery=$this->sql("SELECT * FROM app_WSDiscovery WHERE ID_APP = '".$value["ID"]."'");
            if($resUPnP){
                $salida.="<td>UPnP</td>";
            }else if($resmDNS){
                $salida.="<td>mDNS</td>";
            }else if($resWSDiscovery){
                $salida.="<td>WS-Discovery</td>";
            }
            $salida.="</tr>";
            $contador++;
        }
        $salida.="</table>";
        return $salida;
    }
    function mostrarApp($ID){
        $resUPnP=$this->sql("SELECT * FROM app_UPnP WHERE ID_APP= '".$ID."'");
        $resmDNS=$this->sql("SELECT * FROM app_mDNS WHERE ID_APP= '".$ID."'");
        $resWSDiscovery=$this->sql("SELECT * FROM app_WSDiscovery WHERE ID_APP = '".$ID."'");
        $salida="";
        if($resUPnP){
            $resApp=$this->sql("SELECT * FROM service_UPnP WHERE ID_APP= '".$resUPnP[0]["ID"]."'");
            $salida.="<h1>Service UPnP:</h1>
                <table><tr>
                <th>Name</th>
                <th>ID_Name</th>
                <th>SCPD</th>
                <th>ControlUrl</th>
                <th>EventUrl</th>
                <th>BaseUrl</th>
            </tr>";
            foreach($resApp as $key => $value){
                $salida.="<tr>
                <td>".$value["Name"]."</td>
                <td>".$value["ID_Name"]."</td>
                <td>".$value["SCPD"]."</td>
                <td>".$value["ControlUrl"]."</td>
                <td>".$value["EventUrl"]."</td>
                <td>".$value["BaseUrl"]."</td>
            </tr>";
            }
            $salida.="</table>";
        }else if($resmDNS) {
            $resApp = $this->sql("SELECT * FROM service_mDNS WHERE ID_APP_mDNS= '" . $resmDNS[0]["ID"] . "'");
            $salida .= "<h1>Service mDNS:</h1>
                <table><tr>
                <th>Name</th>
                <th>Type</th>
                <th>Weight</th>
                <th>Priority</th>
                <th>Server</th>
                <th>InterfaceIndex</th>
            </tr>";
            foreach ($resApp as $key => $value) {

                $salida .= "<tr>
                <td>" . $value["Name"] . "</td>
                <td>" . $value["Type"] . "</td>
                <td>" . $value["Weight"] . "</td>
                <td>" . $value["Priority"] . "</td>
                <td>" . $value["Server"] . "</td>
                <td>" . $value["InterfaceIndex"] . "</td>
            </tr>";
            }
            $salida .= "</table>";
        }else if($resWSDiscovery){
            $resApp = $this->sql("SELECT * FROM service_WSDiscovery WHERE ID_APP_WSDiscovery= '" . $resWSDiscovery[0]["ID"] . "'");
            $salida .= "<h1>Service WS-Discovery:</h1>
                <table><tr>
                <th>XAddrs</th>
                <th>EPR</th>
                <th>InstanceId</th>
                <th>MessageNumber</th>
                <th>MetadataVersion</th>
            </tr>";
            foreach ($resApp as $key => $value) {

                $salida .= "<tr>
                <td>" . $value["XAddrs"] . "</td>
                <td>" . $value["EPR"] . "</td>
                <td>" . $value["InstanceId"] . "</td>
                <td>" . $value["MessageNumber"] . "</td>
                <td>" . $value["MetadataVersion"] . "</td>
            </tr>";
            }
            $salida .= "</table>";
        }
        return $salida;
    }
}