from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Define the endpoint where you receive HTTP POST messages
@app.route('/receive_bus_data', methods=['POST'])
def receive_bus_data():
    try:
        # Get the data from the POST request
        data = request.get_json()
        print(data)
        # Edit the data (modify as per your requirements)
        #edited_data = edit_data(data)

        # Post the edited data to another endpoint
        #post_to_endpoint(edited_data, 'https://example.com/other_endpoint')

        # Respond to the original request
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/receive_station_data', methods=['POST'])
def receive_station_data():
    try:
        # Get the data from the POST request
        data = request.get_json()

        tSid = data['id']
        tSlocation = data['location']
        transportStationData= {
            "id": tSid,
            "type": "TransportStation",
            "contractingAuthority": {
                "type": "Property",
                "value": "Municipality of Patras"
            },
            "contractingCompany": {
                "type": "Property",
                "value": "Urban Transports of Patras S.A."
            },
            "location": {
                "type": "GeoProperty",
                "value": {
                    "type": "Point",
                    "coordinates": tSlocation
                }
            },
            "stationType": {
                "type": "Property",
                "value": [
                    "bus"
                ]
            }
        }

        if(data['vID'] == None):
            cFOid = data['cFOID']
            tSdatetimeObserved = data['dtLastObserved']
            transportStationData['dateObserved'] = {
                                                   "type": "DateTime",
                                                   "value": tSdatetimeObserved
                                                  }
            transportStationData['crowdFlowObserved'] = {
                                                        "type": "CrowdFlowObserved",
                                                        "value": cFOid
                                                        }

        if(data['cFOID'] == None):
            vid = data['vID']
            tSdatetimeReported = data['dtLastReported']
            transportStationData['dateLastReported'] = {
                                                       "type": "DateTime",
                                                       "value": tSdatetimeReported
                                                       }
            transportStationData['vehicleLastReported'] = {
                                                           "type": "Vehicle",
                                                           "value": vid
                                                          }

        print(data)

        #post_to_endpoint(edited_data, 'https://example.com/other_endpoint')

        # Respond to the original request
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/receive_crowd_data', methods=['POST'])
def receive_crowd_data():
    try:
        # Get the data from the POST request
        data = request.get_json()

        cFOid = data['id']
        cFOpc = data['value']
        cFOdatetime = data['dateObserved']
        cFObool = False
        if(int(cFOpc) > 20): cFObool = True
        # Create payload
        crowdFlowObservedData = {
            "id": cFOid,
            "type": "CrowdFlowObserved",
            "congested": {
                "type": "Property",
                "value": cFObool
            },
            "dateObserved": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": cFOdatetime
                }
            },
            "peopleCount": {
                "type": "Property",
                "value": cFOpc
            }
        }
        print(data)
        # Edit the data (modify as per your requirements)
        #edited_data = edit_data(data)

        # Post the edited data to another endpoint
        #post_to_endpoint(edited_data, 'https://example.com/other_endpoint')

        # Respond to the original request
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/receive_violation_data', methods=['POST'])
def receive_violation_data():
    try:
        # Get the data from the POST request
        data = request.get_json()
        print(data)
        # Edit the data (modify as per your requirements)
        #edited_data = edit_data(data)

        # Post the edited data to another endpoint
        #post_to_endpoint(edited_data, 'https://example.com/other_endpoint')

        # Respond to the original request
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

# Function to post data to another endpoint
def post_to_endpoint(data, endpoint):
    response = requests.post(endpoint, json=data)
    response.raise_for_status()

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(port=5000)
