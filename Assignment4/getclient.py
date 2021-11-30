# importing the requests library
import requests
#import websocket
import time

while True:
    # importing the requests library
    
    # api-endpoint
    URL = "http://192.168.4.1/"
    
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'api'}
    
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
    
    # extracting data in json format
    #data = r.json()
    
    #print(data)
    time.sleep(3)