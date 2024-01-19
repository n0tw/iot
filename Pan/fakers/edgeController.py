import datetime
from flask import Flask, request, jsonify
import requests
import aiohttp
import asyncio

app = Flask(__name__)

async def get_from_endpoint(endpoint):
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint) as response:
            response.raise_for_status()
            return await response.json()

# Function to post data to another endpoint
async def post_to_endpoint(data, endpoint):
    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, json=data) as response:
            response.raise_for_status()

async def handle_request(data, endpoint):
    try:
        # Edit the data (modify as per your requirements)
        # edited_data = edit_data(data)

        # Asynchronously post the edited data to another endpoint
        await post_to_endpoint(data, endpoint)

        # Respond to the original request
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/receive_bus_data', methods=['POST'])
async def receive_bus_data():
    data = await request.get_json()
    vid = data['vehicleid']
    vcords = data['locations']
    vplate = "LICENCE PLATE"
    vdatetimeObs = datetime.datetime.now().isoformat()
    vcFOid = data['crowdflowid']
    vehicleData = {
        "id": vid,
        "type": "Vehicle",
        "category": {
            "type": "Property",
            "value": [
                "municipalServices"
            ]
        },
        "license_plate": {
            "type": "Property",
            "value": vplate
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": vcords
            }
        },
        "observationDateTime": {
            "type": "Property",
            "value": {
                "@type": "DateTime",
                "@value": vdatetimeObs
            }
        },
        "crowdFlowObserved": {
            "type": "CrowdFlowObserved",
            "value": vcFOid
        },
        "vehicleTrackerDevice": {
            "type": "Property",
            "value": "Installed"
        },
        "vehicleType": {
            "type": "Property",
            "value": "bus"
        }
    }

    extData = await get_from_endpoint("http://localhost:5003/entities"+'/'+str(vid))
    maxVersion = 1
    if extData is not None:
        maxVersion = extData['data'][0]['version'].split(' ')[1]
        for i in range(0,len(extData['data'])):
            if(extData['data'][i]['version'].split(' ')[1] > maxVersion):
                maxVersion = extData['data'][i]['version'].split(' ')[1]
    extDataToPost = vehicleData
    extDataToPost['version'] = "Version "+str(maxVersion)
    await handle_request(extDataToPost, "http://localhost:5003/entity/"+str(vid)+'/version'+str(maxVersion))

    result = await handle_request(vehicleData, "http://150.140.186.118:1026/v2/entities")
    return result

@app.route('/receive_station_data', methods=['POST'])
async def receive_station_data():
    data = await request.get_json()

    tSid = data['id']
    tSlocation = data['location']
    tSname = data['name']

    transportStationData= {
        "id": tSid,
        "type": "TransportStation",
        "name": {
            "type": "String",
            "value": tSname
        },
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
    
    extData = await get_from_endpoint("http://localhost:5003/entities"+'/'+str(tSid))
    maxVersion = 1
    if extData is not None:
        maxVersion = extData['data'][0]['version'].split(' ')[1]
        for i in range(0,len(extData['data'])):
            if(extData['data'][i]['version'].split(' ')[1] > maxVersion):
                maxVersion = extData['data'][i]['version'].split(' ')[1]
    extDataToPost = transportStationData
    extDataToPost['version'] = "Version "+str(maxVersion)
    await handle_request(extDataToPost, "http://localhost:5003/entity/"+str(tSid)+'/version'+str(maxVersion))

    result = await handle_request(transportStationData, "http://150.140.186.118:1026/v2/entities")
    return result

@app.route('/receive_crowd_data', methods=['POST'])
async def receive_crowd_data():
    data = await request.get_json()

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

    extData = await get_from_endpoint("http://localhost:5003/entities"+'/'+str(cFOid))
    maxVersion = 1
    if extData is not None:
        maxVersion = extData['data'][0]['version'].split(' ')[1]
        for i in range(0,len(extData['data'])):
            if(extData['data'][i]['version'].split(' ')[1] > maxVersion):
                maxVersion = extData['data'][i]['version'].split(' ')[1]
    extDataToPost = crowdFlowObservedData
    extDataToPost['version'] = "Version "+str(maxVersion)
    await handle_request(extDataToPost, "http://localhost:5003/entity/"+str(cFOid)+'/version'+str(maxVersion))

    result = await handle_request(crowdFlowObservedData, "http://150.140.186.118:1026/v2/entities")
    return result

@app.route('/receive_violation_data', methods=['POST'])
async def receive_violation_data():
    data = await request.get_json()
    tVid = data['tvid']
    tVdatetime = data['datetime']
    tVplate = data['plate']
    tVtSname = data['stationName']
    tVcords = data['location']
    trafficViolationData = {
        "id": tVid,
        "type": "TrafficViolation",
        "observationDateTime": {
            "type": "Property",
            "value": {
                "@type": "DateTime",
                "@value": tVdatetime
            }
        },
        "description": {
            "type": "Property",
            "value": "Illegal Parking"
        },
        "vehiclePlate": {
            "type": "Property",
            "value":  tVplate
        },
        "transportStation": {
            "type": "transportStation",
            "value": tVtSname
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": tVcords
            }
        }
    }

    extData = await get_from_endpoint("http://localhost:5003/entities"+'/'+str(tVid))
    maxVersion = 1
    if extData is not None:
        maxVersion = extData['data'][0]['version'].split(' ')[1]
        for i in range(0,len(extData['data'])):
            if(extData['data'][i]['version'].split(' ')[1] > maxVersion):
                maxVersion = extData['data'][i]['version'].split(' ')[1]
    extDataToPost = trafficViolationData
    extDataToPost['version'] = "Version "+str(maxVersion)
    await handle_request(extDataToPost, "http://localhost:5003/entity/"+str(tVid)+'/version'+str(maxVersion))

    result = await handle_request(trafficViolationData, "http://150.140.186.118:1026/v2/entities")
    return result

if __name__ == '__main__':
    # Run the Flask app on port 5002
    app.run(port=5002)
