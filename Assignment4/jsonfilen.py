# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 16:40:03 2021

@author: study
"""
#pip install websocket-client
import websocket
import json
import requests

ws = websocket.WebSocket()
ws.connect("ws://192.168.4.1/")
myDict = {"sensor": "temperature", "identifier":"SENS123456789", "value":10, "timestamp": "20/10/2017 10:10:25"}
ws.send(json.dumps(myDict))
result = ws.recv()
print(result)
ws.close()

"""
#GET
api_url = "https://jsonplaceholder.typicode.com/todos/1" #Prøv at ændre den til controllerens IP
response = requests.get(api_url)
response.json()
response.status_code
response.headers["Content-Type"]


#POST
api_url = "https://jsonplaceholder.typicode.com/todos"
todo = {"userId": 1, "title": "Buy milk", "completed": False}
response = requests.post(api_url, json=todo)
response.json()

#PUT The following code sends a PUT request to update an existing todo with new data. 
import requests
api_url = "https://jsonplaceholder.typicode.com/todos/10"
response = requests.get(api_url)
response.json()
#{'userId': 1, 'id': 10, 'title': 'illo est ... aut', 'completed': True}

todo = {"userId": 1, "title": "Wash car", "completed": True}
response = requests.put(api_url, json=todo)
response.json()
#{'userId': 1, 'title': 'Wash car', 'completed': True, 'id': 10}

response.status_code
#200


# PATCH differs from PUT in that it doesn’t completely replace the existing resource. It only modifies the values set in the JSON sent with the request.
import requests
api_url = "https://jsonplaceholder.typicode.com/todos/10"
todo = {"title": "Mow lawn"}
response = requests.patch(api_url, json=todo)
response.json()
#{'userId': 1, 'id': 10, 'title': 'Mow lawn', 'completed': True}
#When you call response.json(), you can see that title was updated to Mow lawn.
>>> response.status_code
200
"""