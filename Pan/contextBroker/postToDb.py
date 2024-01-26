import json
import requests
import connexion
from flask import jsonify
from bson import ObjectId

# FIWARE Context Broker endpoint
#orion_url = "http://localhost:1026/v2/entities"
orion_url = "http://150.140.186.118:1026/v2/entities"

app = connexion.App(__name__, specification_dir='./')
flask_app = app.app

def handle_response(response, success_status_code=200):
    """Handle response from requests and check for errors."""
    if response.status_code == success_status_code:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        response.raise_for_status()

# GET route to retrieve entities by ID
def getEntityRoute(entityId):
    try:
        with flask_app.app_context():
            params = {"id": entityId}
            response = requests.get(orion_url + '/' + entityId, params=params, headers={"Accept": "application/json"})

            entities = handle_response(response)

            if entities:
                print(f"Entity: {entities}")
                return jsonify({'message': f'Entity with ID {entityId} received', 'data': entities})
            else:
                print("No entities found with the specified criteria")
                return jsonify({'message': f'No entities found with ID {entityId}'}), 404

    except requests.RequestException as e:
        print(f"Request failed: {str(e)}")
        return jsonify({'message': 'Error occurred during get'}), 500


def postEntityRoute(entityData):
    try:
        with flask_app.app_context():
            # Send a POST request to the Orion Context Broker
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            response = requests.post(orion_url, headers=headers, data=json.dumps(entityData))

            if response.status_code == 201:
                return jsonify({'message': 'Entity created successfully'})
            else:
                return jsonify({'message': f'Failed to create entity. Status code: {response.status_code}'}), response.status_code
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
    

def patchEntityRoute(entityId, updateData):
    try:
        with flask_app.app_context():
           
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            updateData.pop('id')
            updateData.pop('type')
            payload = {}
            # Update the entity with the provided data
            for key, value in updateData.items():
                if isinstance(value, ObjectId):
                    value = str(value)
                payload[key] = {'value': value}

            # Update the entity in the MongoDB collection
            response = requests.patch(orion_url+'/'+entityId+'/attrs', headers=headers, data=json.dumps(payload))

            return jsonify({'message': f'Entity with ID {entityId} partially updated', 'data': payload})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Error occurred during update'}), 500


# DELETE route to remove entities by ID
def deleteEntityRoute(entityId):
    try:
        with flask_app.app_context():
            params = {"id": entityId}
            response = requests.delete(orion_url + '/' +entityId, params=params, headers = {"Accept": "application/json",})
            entities = handle_response(response)

            if entities:
                print(f"Entity: {entities}")
                return jsonify({'message': f'Entity with ID {entityId} received', 'data': entities})
            else:
                print("No entities found with the specified criteria")
                return jsonify({'message': f'No entities found with ID {entityId}'}), 404

    except requests.RequestException as e:
        print(f"Request failed: {str(e)}")
        return jsonify({'message': 'Error occurred during get'}), 500


if __name__ == '__main__':
    #   Input data
    #   crowdFlowObserverd inputs
    cFOid = "urn:ngsi-ld:CrowdFlowObserved:Blah:1"
    cFObool = False
    cFOdatetime = "2018-08-07T11:10:00/2018-08-07T11:15:00"
    cFOpc = 120
    cFOloctype = "LineString"
    cFOcords = [
                    [
                        -4.73735395519672,
                        41.6538181849672
                    ],
                    [
                        -4.73414858659993,
                        41.6600594193478
                    ],
                    [
                        -4.73447575302641,
                        41.659585195093
                    ]
                ]
    #   trafficViolation inputs
    tVid = "ngsi-ld:Trafficviolation:234R:0212"
    tVdatetime = "2021-03-11T15:51:02+05:30"
    tVplate = "CAR_PLATE"
    tVstation = "trasnport station entity url?"
    tVloctype = "LineString"
    tVcords = [
                    [
                        -4.73735395519672,
                        41.6538181849672
                    ],
                    [
                        -4.73414858659993,
                        41.6600594193478
                    ],
                    [
                        -4.73447575302641,
                        41.659585195093
                    ]
                ]
    
    #   transportStation inputs
    tSid = "urn:ngsi-ld:Station:Station:MNCA-STram-L02-AP-T2"
    tSdatetimeRep = "2020-03-17T08:45:00Z"
    tSvid = "VEHICLE ENTITY ID"
    tSdatetimeObs = "2020-03-17T08:45:00Z"
    tScFOid = "CROWD FLOW OBSERVED ENTITY ID"
    tSdescr = "Description of bus station"
    tSloctype = "Point"
    tScords = [
                43.66481,
                7.196545
            ]
    tSwheelchair = 1
    tSzoneid = "B"
    
    # vehicle inputs
    vid = "urn:ngsi-ld:Vehicle:vehicle:WasteManagement:1"
    vsim = "9942142573"
    vffilled = 6
    vftype = "gas"
    vplate = "KA052134"
    vloctype = "Point"
    vcords = [
                -3.164485591715449,
                40.62785133667262
            ]
    vdatetimeloc = "2018-09-27T12:00:00Z"
    vname = "C Recogida 1"
    vdatetimeObs = "2021-03-11T15:51:02+05:30"
    vcFOid = "CROWD FLOW OBSERVED ENTITY ID"
    vsrvcOnDuty = False
    vsrvcStatus = "onRoute"
    

    #   Payloads
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
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": cFOloctype,
                "coordinates": cFOcords
            }
        },
        "peopleCount": {
            "type": "Property",
            "value": cFOpc
        }
    }

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
            "value": tVstation
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": tVloctype,
                "coordinates": tVcords
            }
        }
    }

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
        "dateLastReported": {
            "type": "DateTime",
            "value": tSdatetimeRep
        },
        "vehicleLastReported": {
            "type": "Vehicle",
            "value": tSvid
        },
        "dateObserved": {
            "type": "DateTime",
            "value": tSdatetimeObs
        },
        "crowdFlowObserved": {
            "type": "CrowdFlowObserved",
            "value": tScFOid
        },
        "description": {
            "type": "Property",
            "value": tSdescr
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": tSloctype,
                "coordinates": tScords
            }
        },
        "stationType": {
            "type": "Property",
            "value": [
                "bus"
            ]
        },
        "wheelChairAccessible": {
            "type": "Property",
            "value": tSwheelchair
        },
        "zoneId": {
            "type": "Property",
            "value": tSzoneid
        }
    }

    vehicleData = {
        "id": vid,
        "type": "Vehicle",
        "category": {
            "type": "Property",
            "value": [
                "municipalServices"
            ]
        },
        "deviceSimNumber": {
            "type": "Property",
            "value": vsim
        },
        "fuelFilled": {
            "type": "Property",
            "value": vffilled
        },
        "fuelType": {
            "type": "Property",
            "value": vftype
        },
        "license_plate": {
            "type": "Property",
            "value": vplate
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": vloctype,
                "coordinates": vcords
            }
        },
        "name": {
            "type": "Property",
            "value": vname
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
        "serviceOnDuty": {
            "type": "Property",
            "value": vsrvcOnDuty,
        },
        "serviceStatus": {
            "type": "Property",
            "value": vsrvcStatus
        },
        "vehicleTrackerDevice": {
            "type": "Property",
            "value": "Installed"
        },
        "vehicleType": {
            "type": "Property",
            "value": "bus"
        },
    }

    
    # Any method we want to use:

    #postEntityRoute(transportStationData)
    #patchEntityRoute(cFOid, crowdFlowObservedData)
    #postEntityRoute(crowdFlowObservedData)
