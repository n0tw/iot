import itertools
import requests
from flask import Flask, jsonify, request
import schedule
import time
import datetime

app = Flask(__name__)

# Shared variable to store the dynamic data
shared_dynamic_data = {'value': None}

crowdFlowObservedIDs = []
transportStationIDs = []
for i in range(1,33):
    crowdFlowObservedIDs.append("urn:ngsi-ld:CrowdFlowObserved:Station:"+str(i))
    transportStationIDs.append("urn:ngsi-ld:Station:Station:"+str(i))

transportStationNames = ["Ermou",
                        "Agiou Nikolaou",
                        "Zaimi",
                        "Old Arsakeio",
                        "Pyrosvestiou Square",
                        "Favierou",
                        "Maratou",
                        "Kourtesi",
                        "Fillppa",
                        "1st Cemetery",
                        "Anthoupoli",
                        "OGA",
                        "Aretha (to University)",
                        "Aretha",
                        "Intracom",
                        "Kotroni",
                        "Mihaniki Kalliergeia",
                        "Mihaniki Kalliergeia 2",
                        "Koridalleos",
                        "Psistaria",
                        "Bissarionos",
                        "Proastio",
                        "Mandreka",
                        "Tofalos Stadium",
                        "Haradros River",
                        "University of Patras Chancellor's Office",
                        "Polytechnic",
                        "Conference Center",
                        "Physics Department",
                        "Geology Department",
                        "Medicine",
                        "Hospital"]

tSlocations = [ [38.24674692664068, 21.73598679633868],
                [38.24758985475257, 21.737535367031022],
                [38.24902222935668, 21.739305624967397],
                [38.250230270712024, 21.740810116383948],
                [38.25168834237874, 21.74273898930706],
                [38.25303006552498, 21.744066682766164],
                [38.2552359603907, 21.74591878456181],
                [38.257312205684094, 21.74801002744799],
                [38.25880554830628, 21.75061789742214],
                [38.260978875703046, 21.752348744111824],
                [38.261362722360786, 21.753829900052864],
                [38.26467030130779, 21.754750337049213],
                [38.266083069968, 21.756725673266818],
                [38.2669037276182, 21.75758606932094],
                [38.26946462223079, 21.758252269487343],
                [38.2709601921641, 21.75870100955657],
                [38.27312923195606, 21.760069226877345],
                [38.274935564361776, 21.762233737852593],
                [38.2769257058954, 21.764604917853518],
                [38.27785469703166, 21.76559210109097],
                [38.27909220240962, 21.76707233421115],
                [38.28046811582278, 21.768750287981504],
                [38.28217119203374, 21.771219124397756],
                [38.28438597032206, 21.772710045166257],
                [38.286147677506634, 21.774788784038343],
                [38.286200499007656, 21.78605393759909],
                [38.287957277337824, 21.786551680608497],
                [38.289797915897964, 21.78494487258972],
                [38.29171454261186, 21.786995974703636],
                [38.29367831146375, 21.790510240924757],
                [38.294454365685155, 21.791879869420182],
                [38.29649522541104, 21.795133184452613]]

# Iterator for cycling through the values
values_iterator = itertools.cycle(['5', '20', '15'])

# Define the endpoint to receive data
@app.route('/receive_data', methods=['POST'])
def receive_data():
    global transportStationNames
    global transportStationIDs
    try:
        # Get the data from the POST request
        data = request.get_json()
        index = transportStationNames.index(data['stationName'])
        # Set the shared dynamic data based on received data
        set_shared_dynamic_data(data)

        # Identify transportStationID with the vehicleID received and post
        dataToPost = {'id': transportStationIDs[index], 'vID': "VehicleID", "dtLastReported": datetime.datetime.now().isoformat(), 
                      'cFOID': None, "dtLastObserved":  None, 'location': data['stationLocation'], 'name': data['stationName']}
        # Post the received data to the edge controller
        post_to_edge_controller(data)

        # Respond to the original request
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Function to set the shared dynamic data based on received data
def set_shared_dynamic_data(data):
    # Example: Set the 'value' key from received data to the shared variable
    global shared_dynamic_data
    shared_dynamic_data = {'value': data.get('value')}

# Function to post data to the edge controller
def post_to_edge_controller(data):
    edge_controller_url = 'http://localhost:5000/receive_station_data'  # Adjust the URL as needed
    response = requests.post(edge_controller_url, json=data)
    response.raise_for_status()

# Function to post data to a different endpoint every 5 seconds
def post_periodically():
    # Use the shared dynamic data
    global shared_dynamic_data
    global values_iterator
    global crowdFlowObservedIDs
    global transportStationIDs
    global transportStationNames
    global tSlocations

    edge_controller_url = 'http://localhost:5000/receive_crowd_data'  # Adjust the URL as needed

    busLocation = shared_dynamic_data

    dynamic_value = next(values_iterator)

    for j in range(1,33):
        # Get the next value from the cycle
        dynamic_data = {'id': crowdFlowObservedIDs[j], 'value': dynamic_value, 'dateObserved': datetime.datetime.now().isoformat()}

        if(busLocation['value'] != None):
            dynamic_data = {'id': "CrowdFlowDataID", 'value': 10, 'dateObserved': datetime.datetime.now().isoformat()}

        response = requests.post(edge_controller_url, json=dynamic_data)
        response.raise_for_status()

        second_endpoint_url = 'http://localhost:5000/receive_station_data'
        # (+) add for loop for all transportStationIDs (and cFOIDs)
        response2 = request.post(second_endpoint_url, json={'id': transportStationIDs[j], 'vID': None,
                                                            "dtLastReported": None, 
                                                            'cFOID': crowdFlowObservedIDs[j],
                                                            "dtLastObserved":  datetime.datetime.now().isoformat(),
                                                            'location': tSlocations[j],
                                                            'name': transportStationNames[j]})
        response2.raise_for_status()

# Schedule the periodic job
schedule.every(5).seconds.do(post_periodically)

# Function to run the scheduled jobs
def run_scheduled_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Run the Flask app on port 5001 in a separate thread
    from threading import Thread
    Thread(target=app.run, kwargs={'port': 5001}).start()

    # Run the scheduled jobs in the main thread
    run_scheduled_jobs()
