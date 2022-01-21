<?php
error_reporting(0);

require("accesoSql.php");

$json=file_get_contents('php://input');
echo $json."\n";
echo "xddd\n";


$jsonDecoded=json_decode($json,true);
print $jsonDecoded;
$clave=$jsonDecoded["Peticion"];
$info=$jsonDecoded["info"];
$AccesoSql=new accesoSql();
echo "\nhola ".$clave;
//Faltaría conseguir json para enviar de forma rapida desde el rest client
//cosas capadas de ejecución
if($clave=="UPnP"||$clave=="mDNS"||$clave=="WS-Discovery"||$clave=="Nmap"){
    echo "jsond: ".$jsonDecoded."\n\n";

    $r=$AccesoSql->anyadirBase($info,$clave);
	echo $r;
}
if($_GET["APP"]){
    $r=$AccesoSql->mostrarApp($_GET["APP"]);
    echo $r;
}



