<html>
 
<head>
    <title>Dispositivo</title>  
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <link rel="stylesheet" href="bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
    <link href="estilo.css" rel="stylesheet" type="text/css" />

    <script src="jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
    <script src="bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
    <script src="scriptPags.js" type="text/javascript"></script>
    
</head>
 
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-info navegador">
    <title class="navbar-brand">Exploracion IoT</title>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="Dispositivos.php">Ir a inicio</a>
      </li>
      <li class="nav-item active dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Protocolos
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="UPnPs.php">UPnP</a>
          <a class="dropdown-item" href="mDNSs.php">mDNS</a>
          <a class="dropdown-item" href="WS-Discoverys.php">WS-Discovery</a>

        </div>
      </li>
    </ul>
    <ul class="navbar-nav">
    <li class="nav-item active dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown2" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Recursos
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">             
            <a class="dropdown-item" href="https://github.com/sdelgj00/Detecci-n-de-dispositivos-y-servicios-IoT"><img src="githubIcon.png" class="icon"></img> Detector IoT</a>
          <a class="dropdown-item" href="https://github.com/sdelgj00/Servidor_deteccion_de_dispositivos_y_servicios_IoT"><img src="githubIcon.png" class="icon"></img> Servidor</a>
          <a class="dropdown-item" href="mailto:sdelgj00@estudiantes.unileon.es"><img src="gmail.png" class="icon"></img> Contacto</a>
        </div>
      </li>
    <ul>
</nav>

    <br>
    <div class="page-header">
        <h1 class="h1 titulo">Dispositivo <?php echo $_GET['ip'];?></h1>
        <hr>
    </div>

    <br>
    <h2 class="titulo">Puertos</h2>
    <hr>
    <br>

    <table class="text-center table-striped table-responsive-sm table-w contentTable">
        <tr class="bg-warning flex-column">
			<th>ID</th><th>Port</th><th>Type</th><th>State</th><th>Name</th><th>Product</th><th>Version</th><th>Extra Info</th><th>Conf</th><th>CPE</th>
		</tr>
        <tbody  class='table-dark bg-dark flex-column '>
        <?php
        require("accesoSql.php");
        $accesosql=new accesoSql();
        $puertos=$accesosql->sql("SELECT * FROM port WHERE IP= '".$_GET['ip']."'");
        foreach($puertos as $i){
            echo "<tr onclick=irPort(".$i["Port"].",".$i["ID"].")>
                <td>".$i["ID"]."</td><td>".$i["Port"]."</td><td>".$i["Type"]."</td><td>".$i["State"]."</td><td>".$i["Name"]."</td><td>".$i["Product"]."</td><td>".$i["Version"]."</td><td>".$i["ExtraInfor"]."</td><td>".$i["Conf"]."</td><td>".$i["Cpe"]."</td>
            </tr>";
        }
    ?>
      </tbody></table>

    <br>
    <h2 class="titulo">OS</h2>
    <hr>
    <br>

    <table class="text-center table-striped table-responsive-sm table-w contentTable">
        <tr class="bg-warning flex-column">
			<th>ID</th><th>Name</th><th>Accuracy</th><th>Line</th>
		</tr>
        <tbody  class='table-dark bg-dark flex-column '>
        <?php
        $accesosql=new accesoSql();
        $os_script=$accesosql->sql("SELECT * FROM os_script WHERE IP= '".$_GET['ip']."'");
        foreach($os_script as $i){
            echo "<tr onclick=irOS(".$i["ID"].")>
                <td>".$i["ID"]."</td><td>".$i["Name"]."</td><td>".$i["Accuracy"]."</td><td>".$i["Line"]."</td>
            </tr>";
        }
    ?>
 	</tbody></table>
     
     <br>
     <h2 class="titulo">UPnP</h2>
     <hr>
     <br>

     <table class="text-center table-striped table-responsive-sm table-w contentTable">
     <tr class="bg-warning flex-column">
			<th>ID App</th><th>ID App UPnP</th><th>Port</th><th>Name</th>
		</tr>
        <tbody  class='table-dark bg-dark flex-column '>
        <?php
        $accesosql=new accesoSql();
        $apps=$accesosql->sql("SELECT * FROM app WHERE IP= '".$_GET['ip']."'");
        foreach($apps as $i){
            $existeAppUPnP=$accesosql->sql("SELECT * FROM app_upnp WHERE ID_APP ='".$i["ID"]."'");
            if(count($existeAppUPnP)>0){
                echo "<tr onclick=irUPnP(".$existeAppUPnP[0]["ID"].",'".$_GET["ip"]."',".$i["Port"].")>
                    <td>".$i["ID"]."</td><td>".$existeAppUPnP[0]["ID"]."</td><td>".$i["Port"]."</td><td>".$existeAppUPnP[0]["Name"]."</td>
                </tr>";
            }
        }
    ?>
 	</tbody></table>
          
     <br>
     <h2 class="titulo">mDNS</h2>
     <hr>
     <br>

     <table class="text-center table-striped table-responsive-sm table-w contentTable">
     <tr class="bg-warning flex-column">
			<th>ID App</th><th>ID App mDNS</th>
		</tr>
        <tbody  class='table-dark bg-dark flex-column '>
        <?php
        $accesosql=new accesoSql();
        foreach($apps as $i){
            $existeAppMDNS=$accesosql->sql("SELECT * FROM app_mdns WHERE ID_APP ='".$i["ID"]."'");
            if(count($existeAppMDNS)>0){
                echo "<tr onclick=irMDNS(".$existeAppMDNS[0]["ID"].",'".$_GET["ip"]."',".$i["Port"].")>
                    <td>".$i["ID"]."</td><td>".$existeAppMDNS[0]["ID"]."</td>
                </tr>";
            }
        }
    ?>
 	</tbody></table>
             
     <br>
     <h2 class="titulo">WS-Discovery</h2>
     <hr>
     <br>

     <table class="text-center table-striped table-responsive-sm table-w contentTable">
     <tr class="bg-warning flex-column">
			<th>ID app</th><th>ID app WS-Discovery</th>
		</tr>
        <tbody  class='table-dark bg-dark flex-column '>
        <?php
        $accesosql=new accesoSql();
        foreach($apps as $i){
            $existeAppWSDiscovery=$accesosql->sql("SELECT * FROM app_wsdiscovery WHERE ID_APP ='".$i["ID"]."'");
            if(count($existeAppWSDiscovery)>0){
                /*echo "<tr onclick=irMDNS(".$existeAppWSDiscovery[0]["ID"].",'".$_GET["ip"]."',".$i["Port"].")>
                    <td>".$i["ID"]."</td><td>".$existeAppWSDiscovery[0]["ID"]."</td><td>".$existeAppWSDiscovery[0]["EPR"]."</td>
                    <td>".$existeAppWSDiscovery[0]["InstanceID"]."</td><td>".$existeAppWSDiscovery[0]["MessageNumber"]."</td><td>".$existeAppWSDiscovery[0]["MetadataVersion"]."</td>
                    <td>".$existeAppWSDiscovery[0]["XAddrs"]."</td>
                </tr>";
                
                
                */
                echo "<tr onclick=irWSDiscovery(".$existeAppWSDiscovery[0]["ID"].",'".$_GET["ip"]."',".$i["Port"].")>
                    <td>".$i["ID"]."</td><td>".$existeAppWSDiscovery[0]["ID"]."</td>
                </tr>";
            }
        }
    ?>
 	</tbody></table><br>

</body>
</html>