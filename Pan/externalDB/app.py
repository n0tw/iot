from datetime import timedelta, timezone
import datetime
from pymongo import MongoClient
import methods

# MongoDB configuration
client = MongoClient("mongodb://localhost:27017/") 

# Select the database
db = client["externalDB"]

# Select the collection within the database
collection = db['collection_of_historical_data']

if __name__ == '__main__':
    #   Input data
    #   crowdFlowObserverd inputs
    cFOid = "urn:ngsi-ld:CrowdFlowObserved:Valladolid_1"
    cFObool = False
    cFOdatetime = datetime.datetime.fromisoformat("2018-08-07T11:10:00").isoformat()
    cFOpc = 105
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
    tVdatetime = datetime.datetime.fromisoformat("2021-03-11T15:51:02+05:30").isoformat()
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
    tSdatetimeRep = datetime.datetime.fromisoformat("2020-03-17T08:45:00Z").isoformat()
    tSvid = "VEHICLE ENTITY ID"
    tSdatetimeObs = datetime.datetime.fromisoformat("2020-03-17T08:45:00Z").isoformat()
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
    vdatetimeloc = datetime.datetime.fromisoformat("2018-09-27T12:00:00Z").isoformat()
    vname = "C Recogida 1"
    vdatetimeObs = datetime.datetime.fromisoformat("2021-03-11T15:51:02+05:30").isoformat()
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
            },
            "observedAt": vdatetimeloc
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

    offset_minutes = 0
    # Creating a timezone object
    tz = timezone(timedelta(minutes=offset_minutes))
    methods.postEntityRoute(crowdFlowObservedData, collection)
    methods.getEntitiesByTimeRoute(tSid,"TransportStation",2020,3,11,15,31,2,2023,4,5,1,5,2,tz,collection)
    