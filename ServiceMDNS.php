<html>
 
<head>
    <title>Servicio mDNS</title>  
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
        <h1 class="h1 titulo"><?php echo str_replace("_"," - ",$_GET["Title"]);?></h1>
        <hr>
    </div>

    <br>
    <h2 class="titulo">Vulnerabilities</h2>
    <hr>
    <br>

     <table class="text-center table-striped table-responsive-sm table-w contentTable">
        <tr class="bg-warning flex-column">
			<th>ID</th><th>Publish Date</th><th>Last Modified Date</th><th>Description</th><th>Lang</th><th>bmv2severity </th><th>bmv2explitabilityScore</th>
            <th>bmv2impactScore</th><th>bmv2acInsufInfo</th><th>bmv2obtainAllPrivilege</th><th>bmv2obtainUserPrivilege</th><th>bmv2obtainOtherPrivilege</th><th>bmv2userInteractionRequired</th>
            <th>bmv2accessVector</th><th>bmv2accessComplexity</th><th>bmv2authentication</th><th>bmv2confidentialityImpact</th><th>bmv2integrityImpact</th><th>bmv2availabilityImpact</th><th>bmv2baseScore</th>
            <th>bmv3exploitabilityScore</th><th>bmv3impactScore</th><th>bmv3attackVector</th><th>bmv3attackComplexity</th><th>bmv3privilegesRequired</th><th>bmv3userInteraction</th><th>bmv3scope</th>
            <th>bmv3confidentialImpact</th><th>bmv3integrityImpact</th><th>bmv3availabilityImpact</th><th>bmv3baseScore</th><th>bmv3baseSeverity</th>
		</tr>
        <tbody  class='table-dark bg-dark flex-column '>
        <?php
        require("accesoSql.php");
        $accesosql=new accesoSql();
        $vuls;
        if($_GET["Prot"]=="UPnP"){
            $vuls=$accesosql->sql("SELECT * FROM vulnerability_upnp WHERE ID_SERVICE= '".$_GET['id']."'");
        }else if($_GET["Prot"]=="mDNS"){
            $vuls=$accesosql->sql("SELECT * FROM vulnerability_mdns WHERE ID_SERVICE= '".$_GET['id']."'");
        }else if($_GET["Prot"]=="WS-Discovery"){
            $vuls=$accesosql->sql("SELECT * FROM vulnerability_wsdiscovery WHERE ID_SERVICE= '".$_GET['id']."'");
        }
        foreach($vuls as $i){
            echo "<tr>
                <td>".$i["ID"]."</td><td>".$i["PublishDate"]."</td><td>".$i["LastModifiedDate"]."</td><td>".$i["Description"]."</td><td>".$i["Lang"]."</td><td>".$i["bmv2severity"]."</td><td>".$i["bmv2explitabilityScore"]."</td>
                <td>".$i["bmv2impactScore"]."</td><td>".$i["bmv2acInsufInfo"]."</td><td>".$i["bmv2obtainAllPrivilege"]."</td><td>".$i["bmv2obtainUserPrivilege"]."</td><td>".$i["bmv2obtainOtherPrivilege"]."</td>
                <td>".$i["bmv2userInteractionRequired"]."</td><td>".$i["bmv2accessVector"]."</td><td>".$i["bmv2accessComplexity"]."</td><td>".$i["bmv2authentication"]."</td><td>".$i["bmv2confidentialityImpact"]."</td>
                <td>".$i["bmv2integrityImpact"]."</td><td>".$i["bmv2availabilityImpact"]."</td><td>".$i["bmv2baseScore"]."</td><td>".$i["bmv3exploitabilityScore"]."</td><td>".$i["bmv3impactScore"]."</td><td>".$i["bmv3attackVector"]."</td>
                <td>".$i["bmv3attackComplexity"]."</td><td>".$i["bmv3privilegesRequired"]."</td><td>".$i["bmv3userInteraction"]."</td><td>".$i["bmv3scope"]."</td><td>".$i["bmv3confidentialImpact"]."</td><td>".$i["bmv3integrityImpact"]."</td>
                <td>".$i["bmv3availabilityImpact"]."</td><td>".$i["bmv3baseScore"]."</td><td>".$i["bmv3baseSeverity"]."</td>
            </tr>";
        }
    ?>
      </tbody></table>
    <br>
    <h2 class="titulo">Properties</h2>
    <hr>
    <br>
    <table class="text-center table-striped table-responsive-sm table-w contentTable">
        <tr class="bg-warning flex-column">
			<th>ID</th><th>Key</th><th>Value</th>
		</tr>
        <tbody  class='table-dark bg-dark flex-column '>
    <?php
    $prop=$accesosql->sql("SELECT * FROM property_mdns WHERE ID_SERVICE_MDNS= '".$_GET['id']."'");
    foreach($prop as $i){
        echo "<tr>
            <td>".$i["ID"]."</td><td>".$i["Llave"]."</td><td>".$i["Valor"]."</td>
        </tr>";
    }   
    ?>
 	</tbody></table><br>
 
</body>
</html>