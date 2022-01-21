function dispositivo(idApp){
    let div= document.getElementById("divTabla");
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            //console.log(this.responseText);
            //var curr = window.open("",'Pasatiempo');
            //div.write(this.response);
            //setTimeout(() => {  creaTabla(); }, 200);
            console.log(this.response);
            div.innerHTML=this.response;
            //div.innerHTML="<h1>hola</h1>";

        }
    };
    xmlhttp.open("GET", "controlador.php?APP="+idApp, true);
    xmlhttp.send();
}
function irDispositivo(){
    console.log(IP);
    document.location.href="Dispositivo.php?"+IP;
}

/*function dispositivo(idApp){
    console.log("xd");
    let div= document.getElementById("divTabla");
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            //console.log(this.responseText);
            //var curr = window.open("",'Pasatiempo');
            //div.write(this.response);
            //setTimeout(() => {  creaTabla(); }, 200);
            div.innerHTML="<h1>hola</h1>";

        }
    };
    xmlhttp.open("GET", "controlador.php?APP="+idApp, true);
    xmlhttp.send();
}

 */