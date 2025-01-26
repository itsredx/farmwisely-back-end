import requests
import sys

import json
                

response = requests.request("GET", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Gwale%20kano%20Nigeria?unitGroup=metric&include=days%2Chours%2Calerts%2Ccurrent&key=F7LAB8FDDTCN5ABPRK5ND23L6&contentType=json")
if response.status_code!=200:
  print('Unexpected Status code: ', response.status_code)
  sys.exit()  


# Parse the results as JSON
jsonData = response.json()
print(jsonData)