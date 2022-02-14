import requests
import datetime
class Vulnerabilidades:
    dispositivos={}
    url = "https://services.nvd.nist.gov/rest/json/cves/1.0/"
    urlCWE = "https://www.opencve.io/api/cwe/"
    def __init__(self, dispositivos):
        self.dispositivos=dispositivos

    def obtenerCPE(self,IP):
        for i in self.dispositivos['Nmap']:
            if i == IP:
                try:
                    return self.dispositivos['Nmap'][IP]['osmatch'][0]['osclass'][0]['cpe'][0]+'*'
                except:
                    return ''
        return ''
    def anyadirCWE(self, req):
        for i in req['result']['CVE_Items']:
            if i['cve']['problemtype']['problemtype_data'][0]['description'][0]['value']!= '':
                resp = requests.get(
                    self.urlCWE+i['cve']['problemtype']['problemtype_data'][0]['description'][0]['value'],
                    auth=("sully99", "3@b4EY@QxavktEu")
                )
                resp=resp.json()
                i['CWE_desc']=resp['name']
                cweRed=str(i['cve']['problemtype']['problemtype_data'][0]['description'][0]['value']).replace('CWE-','')
                i['CWE_url']='https://cwe.mitre.org/data/definitions/'+cweRed+'.html'
        return req
    def anyadirURL(self, req):
        for i in req['result']['CVE_Items']:
            i['CVE_url']='https://nvd.nist.gov/vuln/detail/'+i['cve']['CVE_data_meta']['ID']
        return req
    def consultarVulnerabilidades(self,servicio, IP):

        if (len(servicio) >= 3):
            # Selecciono las vulnerabilidades encontradas en los últimos 3 meses en los servicios:
            fecha = datetime.datetime.now()
            fechaAhora = fecha.strftime("%Y-%m-%dT%H:%M:%S:000 UTC-00:00")
            fechaHace120dias = fecha - datetime.timedelta(days=120)
            fechaHace120dias = fechaHace120dias.strftime("%Y-%m-%dT%H:%M:%S:000 UTC-00:00")

            jsonVulnerabil = {"apiKey":"cbc2a11a-7326-4b43-94c1-a9af08db23c2","keyword": servicio, "resultsPerPage": 40, "pubStartDate": fechaHace120dias,
                              "pubEndDate": fechaAhora, "cpeMatchString":self.obtenerCPE(IP)}
            print(jsonVulnerabil)
            r = requests.get(self.url, params=jsonVulnerabil)
            r=r.json()
            r=self.anyadirCWE(r)
            r=self.anyadirURL(r)
            jsonVul = r
            # este if es para sí con la anterior búsqueda no ha encontrado vulnerabilidades
            if (jsonVul["totalResults"] == 0):
                jsonVulnerabil = {"apiKey":"cbc2a11a-7326-4b43-94c1-a9af08db23c2", "keyword": servicio, "resultsPerPage": 10, "cpeMatchString":self.obtenerCPE(IP)}
                r = requests.get(self.url, params=jsonVulnerabil)
                r = r.json()

                r=self.anyadirCWE(r)
                r=self.anyadirURL(r)

                return r
            else:
                return r
        else:
            # este else es para si no puede encontrar vulnerabilidades. En este caso, se crea un result vacío
            fecha = datetime.datetime.now()
            fechaAhora = fecha.strftime("%Y-%m-%dT%H:%M:%SZ")
            return {"resultsPerPage": 0, "startIndex": 0, "totalResults": 0, "result": {}}
