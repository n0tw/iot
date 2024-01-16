import itertools
import requests
from flask import Flask, jsonify, request
import schedule
import time
import datetime

app = Flask(__name__)

# Shared variable to store the dynamic data
shared_dynamic_data = {'value': None}

# Iterator for cycling through the values
values_iterator = itertools.cycle(['5', '20', '15'])

# Define the endpoint to receive data
@app.route('/receive_data', methods=['POST'])
def receive_data():
    try:
        # Get the data from the POST request
        data = request.get_json()

        # Set the shared dynamic data based on received data
        set_shared_dynamic_data(data)

        # dataToPost = {'id': "TransportStationID", 'vID': "VehicleID", "dtLastReported": datetime.datetime.now().isoformat(), 
        #                                                "dtLastObserved":  None}
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
    edge_controller_url = 'http://localhost:5000/receive_crowd_data'  # Adjust the URL as needed

    # Use the shared dynamic data
    global shared_dynamic_data
    busLocation = shared_dynamic_data

    global values_iterator
    dynamic_value = next(values_iterator)

    # Get the next value from the cycle
    dynamic_data = {'id': "CrowdFlowDataID", 'value': dynamic_value, 'location': None}

    if(busLocation['value'] != None):
        dynamic_data = {'id': "CrowdFlowDataID", 'value': 10, 'location': busLocation['value']}

    response = requests.post(edge_controller_url, json=dynamic_data)
    response.raise_for_status()

    second_endpoint_url = 'your_second_endpoint_url_here'
    response2 = request.post(second_endpoint_url, json={'id': "TransportStationID", 'vID': "VehicleID", "dtLastReported": "None", 
                                                        "dtLastObserved":  datetime.datetime.now().isoformat()})
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
