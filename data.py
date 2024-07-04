import requests
import json
from urllib.parse import urlparse 
def datav2(url):
    result = requests.get(url)
    parsed = urlparse(url)
    uri = parsed.path
    nom_ficher= uri.replace("/","_")
    payload = {
        'endpoint' : uri,
        'data' : result.json()
    }
    payload= json.dumps(payload, indent=4)
    
    with open(nom_ficher+".json", "w") as outfile:
        outfile.write(payload)
    
    return result 
  

print(datav2("https://api.openweathermap.org/data/2.5/weather?lat=45.75&lon=4.85&appid=ee7036077ff115f4e0a8c12615218478"))