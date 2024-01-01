import json
import datetime as dt
from bson import json_util
from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/get_data', methods=['GET'])
# GET route to retrieve entities by ID
def getEntityRoute(entityId, collection):
    # Get the MongoDB collection
    data = []
    try:
        # Find the entity by custom_id
        for existing_entity in collection.find({'id': entityId}):
            data.append(existing_entity)

        if len(list(collection.find({'id': entityId}))) == 0:
            return print({'message': f'Entity with ID {entityId} not found'}, 404)

        return print({'message': f'Entity with ID {entityId} received', 'data': data})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return print({'message': 'Error occurred during get'}, 500)
    
@app.route('/get_data_by_time', methods=['GET'])
def getEntitiesByTimeRoute(entityId, entityType, initYear, initMonth, initDay, initHour, initMinute, initSecond,
                           endYear ,endMonth, endDay, endHour, endMinute, endSecond, tz, collection):
    # Get the MongoDB collection
    data = []
    data2 = []
    diag = [[],[]]
    try:
        # Bulk request for entity CrowdFlowObserved
        if entityType == "CrowdFlowObserved":
            for existing_entity in collection.find({
                                                "dateObserved.value.@value": {
                                                    "$gte": dt.datetime(initYear, initMonth, initDay, 
                                                                        initHour, initMinute, initSecond,0,tzinfo=tz).isoformat(),
                                                    "$lt": dt.datetime(endYear, endMonth, endDay, 
                                                                        endHour, endMinute, endSecond,0,tzinfo=tz).isoformat()
                                                },
                                                "id": entityId
                                                }):
                data.append(existing_entity)
            for x in data:
                diag[0].append(x['dateObserved']['value']['@value'])
                diag[1].append(x['peopleCount']['value'])

            if len(list(collection.find({
                                    "dateObserved.value.@value": {
                                        "$gte": dt.datetime(initYear, initMonth, initDay, 
                                                            initHour, initMinute, initSecond,0,tzinfo=tz).isoformat(),
                                        "$lt": dt.datetime(endYear, endMonth, endDay, 
                                                            endHour, endMinute, endSecond,0,tzinfo=tz).isoformat()
                                    },
                                    "id": entityId
                                    }
                                    ))) == 0:
                print({'message': f'Entity with ID {entityId} or specific DateTime values not found'}, 404)
                return 0
        
        # Bulk request for entity TrafficViolation
        elif entityType == "TrafficViolation":
            for existing_entity in collection.find({
                                                "observationDateTime.value.@value": {
                                                    "$gte": dt.datetime(initYear, initMonth, initDay, 
                                                                        initHour, initMinute, initSecond,0,tzinfo=tz).isoformat(),
                                                    "$lt": dt.datetime(endYear, endMonth, endDay, 
                                                                        endHour, endMinute, endSecond,0,tzinfo=tz).isoformat()
                                                },
                                                "id": entityId
                                                }):
                data.append(existing_entity)
            
            if len(list(collection.find({
                                    "observationDateTime.value.@value": {
                                        "$gte": dt.datetime(initYear, initMonth, initDay, 
                                                            initHour, initMinute, initSecond,0,tzinfo=tz).isoformat(),
                                        "$lt": dt.datetime(endYear, endMonth, endDay, 
                                                            endHour, endMinute, endSecond,0,tzinfo=tz).isoformat()
                                    },
                                    "id": entityId
                                    }
                                    ))) == 0:
                print({'message': f'Entity with ID {entityId} or specific DateTime values not found'}, 404)
                return 0
        
        # Bulk request for entity TransportStation
        elif entityType == "TransportStation":
            # Search by dateLastReported
            for existing_entity in collection.find({
                                                "dateLastReported.value": {
                                                    "$gte": dt.datetime(initYear, initMonth, initDay, 
                                                                        initHour, initMinute, initSecond,0,tzinfo=tz).isoformat(),
                                                    "$lt": dt.datetime(endYear, endMonth, endDay, 
                                                                        endHour, endMinute, endSecond,0,tzinfo=tz).isoformat()
                                                },
                                                "id": entityId
                                                }):
                data.append(existing_entity)
            
            # Search by dateObserved
            for existing_entity2 in collection.find({
                                                "dateObserved.value": {
                                                    "$gte": dt.datetime(initYear, initMonth, initDay, 
                                                                        initHour, initMinute, initSecond,0,tzinfo=tz).isoformat(),
                                                    "$lt": dt.datetime(endYear, endMonth, endDay, 
                                                                        endHour, endMinute, endSecond,0,tzinfo=tz).isoformat()
                                                },
                                                "id": entityId
                                                }):
                data2.append(existing_entity2)

            if (len(list(collection.find({
                                    "dateLastReported.value": {
                                        "$gte": dt.datetime(initYear, initMonth, initDay, 
                                                            initHour, initMinute, initSecond,0,tzinfo=tz).isoformat(),
                                        "$lt": dt.datetime(endYear, endMonth, endDay, 
                                                            endHour, endMinute, endSecond,0,tzinfo=tz).isoformat()
                                    },
                                    "id": entityId
                                    }
                                    ))) == 0) and (len(list(collection.find({
                                    "dateObserved.value": {
                                        "$gte": dt.datetime(initYear, initMonth, initDay, 
                                                            initHour, initMinute, initSecond,0,tzinfo=tz).isoformat(),
                                        "$lt": dt.datetime(endYear, endMonth, endDay, 
                                                            endHour, endMinute, endSecond,0,tzinfo=tz).isoformat()
                                    },
                                    "id": entityId
                                    }
                                    ))) == 0):
                print({'message': f'Entity with ID {entityId} or specific DateTime values not found'}, 404)
                return 0
        
        # Bulk request for entity Vehicle
        elif entityType == "Vehicle":
            for existing_entity in collection.find({
                                                "observationDateTime.value.@value": {
                                                    "$gte": dt.datetime(initYear, initMonth, initDay, 
                                                                        initHour, initMinute, initSecond,0,tzinfo=tz).isoformat(),
                                                    "$lt": dt.datetime(endYear, endMonth, endDay, 
                                                                        endHour, endMinute, endSecond,0,tzinfo=tz).isoformat()
                                                },
                                                "id": entityId
                                                }):
                data.append(existing_entity)

            if len(list(collection.find({
                                    "observationDateTime.value.@value": {
                                        "$gte": dt.datetime(initYear, initMonth, initDay, 
                                                            initHour, initMinute, initSecond,0,tzinfo=tz).isoformat(),
                                        "$lt": dt.datetime(endYear, endMonth, endDay, 
                                                            endHour, endMinute, endSecond,0,tzinfo=tz).isoformat()
                                    },
                                    "id": entityId
                                    }
                                    ))) == 0:
                print({'message': f'Entity with ID {entityId} or specific DateTime values not found'}, 404)
                return 0
            
        else: 
            print("Error: Wrong type.")
            return 0
        print({'message': f'Entity with ID {entityId} received', 'data': data, 'secondary data': data2})
        return {'data': diag}
    
    except Exception as e:
        print(f"Error: {str(e)}")
        print({'message': 'Error occurred during get'}, 500)
        return 0

@app.route('/post_data', methods=['POST'])
def postEntityRoute(data, collection):
    # Example: Insert data into MongoDB using Flask-PyMongo
    givenID = data['id']
    givenVersion = data['version']
    if (collection.find_one({'id': givenID}) != None and collection.find_one({'version': givenVersion}) != None):
        return print({'message': f'Entity with ID {givenID} and version {givenVersion} already exists'})
    collection.insert_one(data)
    return print({'message': 'Entity posted successfully'})

@app.route('/update_data', methods=['PATCH'])
def patchEntityRoute(entityId, updateData, collection):
    # Get the MongoDB collection
    try:
        # Find the entity by custom_id
        existing_entity = collection.find_one({'id': entityId})

        if not existing_entity:
            return print({'message': f'Entity with ID {entityId} not found'}, 404)
        
        entityType = existing_entity['type']

        # Update the entity with the provided data
        for key, value in updateData.items():
            if key in existing_entity:
                existing_entity[key] = value

        existing_entity.pop('id',None)
        existing_entity.pop('type',None)

        json_document = json.loads(json_util.dumps(existing_entity))

        # Update the entity in the MongoDB collection
        collection.update_one({'id': entityId, 'type': entityType}, {'$set': json_document})
        return print({'message': f'Entity with ID {entityId} partially updated', 'data': existing_entity})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return print({'message': 'Error occurred during update'}, 500)

@app.route('/delete_data', methods=['DELETE'])
# DELETE route to remove entities by ID
def deleteEntityRoute(entityId, collection):
    # Get the MongoDB collection
    try:
        # Find the entity by custom_id
        existing_entity = collection.find_one({'id': entityId})

        if not existing_entity:
            return print({'message': f'Entity with ID {entityId} not found'}, 404)
        
        entityObjectId = existing_entity['_id']
        collection.delete_one({'_id': entityObjectId})

        return print({'message': f'Entity with ID {entityId} deleted', 'data': existing_entity})

    except Exception as e:
        print(f"Error: {str(e)}")
        return print({'message': 'Error occurred during delete'}, 500)