import pandas as pd
import threading
import keyboard
import requests
import json

xlsxFilePath = 'C:/Users/pangl/Desktop/GitRepo/Pan/fakers/Routes.xlsx'
df = pd.read_excel(xlsxFilePath)

t = None

def sendFakeLocation(routes,i):
    global t
    busLocation = routes[i]
    if(i == len(routes)):
        i = 0
    else: i += 1
    response = requests.post(url='http://localhost:5001/receive_data', headers={
    "content-type": "application/json"},  data=json.dumps(busLocation))
    # (if(busLocation[0] == busLocation[2]): post to TransportStation.dateLastReported the datetime.now())
    print(busLocation)
    t = threading.Timer(10.0, sendFakeLocation)
    t.start()


start = 0
routesList = df.values.tolist()
sendFakeLocation(routesList,start)
while True:
    if keyboard.read_key() == "q":
        t.cancel()
        break



