import datetime as dt
import json
import connexion
from flask_cors import CORS
from flask import jsonify, request
from flask_pymongo import PyMongo
from bson import json_util

app = connexion.App(__name__, specification_dir='./')
app.add_api('swagger.yml', resolver=connexion.RestyResolver('api'))

# MongoDB configuration
app.app.config['MONGO_URI'] = 'mongodb://localhost:27017/your_database_name'
mongo = PyMongo(app.app)

# GET route to retrieve entities by ID
@app.route('/get_entity', methods=['GET'])
def getEntityRoute():
    entityId = request.args.get('id')

    # Get the MongoDB collection
    collection = mongo.db['your_collection']
    data = []
    try:
        # Find the entity by custom_id
        for existing_entity in collection.find({'id': entityId}):
            existing_entity.pop('_id',None)
            data.append(existing_entity)

        if len(list(collection.find({'id': entityId}))) == 0:
            return jsonify({'message': f'Entity with ID {entityId} not found'}), 404

        return jsonify({'message': f'Entity with ID {entityId} received', 'data': data})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Error occurred during get'}), 500
    

@app.route('/get_entities_by_time', methods=['GET'])
def getEntitiesByTimeRoute():
    entityId = request.args.get('id')
    initYear = int(request.args.get('Year from'))
    initMonth = int(request.args.get('Month from'))
    initDay = int(request.args.get('Day from'))
    initHour = int(request.args.get('Hour from'))
    initMinute = int(request.args.get('Minute from'))
    initSecond = int(request.args.get('Second from'))

    endYear = int(request.args.get('Year to'))
    endMonth = int(request.args.get('Month to'))
    endDay = int(request.args.get('Day to'))
    endHour = int(request.args.get('Hour to'))
    endMinute = int(request.args.get('Minute to'))
    endSecond = int(request.args.get('Second to'))

    # Get the MongoDB collection
    collection = mongo.db['your_collection']
    data = []
    try:
        # Find the entity by custom_id, date and time
        for existing_entity in collection.find({
                                                "dateObserved":
                                                    {
                                                    "type": "datetime",
                                                    "value": 
                                                    {
                                                        "$gte": dt.datetime(initYear, initMonth, initDay, 
                                                                            initHour, initMinute, initSecond),
                                                        "$lt": dt.datetime(endYear, endMonth, endDay, 
                                                                            endHour, endMinute, endSecond)
                                                    }
                                                    },
                                                "id": entityId
                                                }):
            existing_entity.pop('_id',None)
            data.append(existing_entity)
        print(list(collection.find({
                                    "dateObserved": 
                                        {
                                        "type": "datetime",
                                        "value": 
                                            {
                                            "$gte": dt.datetime(initYear, initMonth, initDay, 
                                                                initHour, initMinute, initSecond),
                                            "$lt": dt.datetime(endYear, endMonth, endDay, 
                                                                endHour, endMinute, endSecond)
                                            }
                                        },
                                    "id": entityId
                                    }
                                    )))
        if len(list(collection.find({
                                    "dateObserved": 
                                        {
                                        "type": "datetime",
                                        "value": 
                                            {
                                            "$gte": dt.datetime(initYear, initMonth, initDay, 
                                                                initHour, initMinute, initSecond),
                                            "$lt": dt.datetime(endYear, endMonth, endDay, 
                                                                endHour, endMinute, endSecond)
                                            }
                                        },
                                    "id": entityId
                                    }
                                    ))) == 0:
            print(dt.datetime(initYear,initMonth,initDay,initHour,initMinute,initSecond))
            print(dt.datetime(endYear,endMonth,endDay,endHour,endMinute,endSecond))
            return jsonify({'message': f'Entity with ID {entityId} not found'}), 404

        return jsonify({'message': f'Entity with ID {entityId} received', 'data': data})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Error occurred during get'}), 500


@app.route('/post_entity', methods=['POST'])
def postEntityRoute():
    data = request.json

    # Example: Insert data into MongoDB using Flask-PyMongo
    mongo.db.your_collection.insert_one(data)

    return jsonify({'message': 'Entity posted successfully'})

@app.route('/update_entity', methods=['PATCH'])
def patchEntityRoute():
    entityId = str(request.args.get('entityId'))

    # Get the MongoDB collection
    collection = mongo.db['your_collection']

    try:
        # Find the entity by custom_id
        existing_entity = collection.find_one({'id': entityId})

        if not existing_entity:
            return jsonify({'message': f'Entity with ID {entityId} not found'}), 404

        entityObjectId = existing_entity['_id']

        # Update the entity with the provided data
        update_data = request.json
        for key, value in update_data.items():
            if key in existing_entity:
                existing_entity[key] = value
        
        existing_entity.pop('_id',None)
        
        json_document = json.loads(json_util.dumps(existing_entity))

        # Update the entity in the MongoDB collection
        collection.update_one({'_id': entityObjectId}, {'$set': json_document})

        return jsonify({'message': f'Entity with ID {entityId} partially updated', 'data': existing_entity})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Error occurred during update'}), 500


# DELETE route to remove entities by ID
@app.route('/delete_entity', methods=['DELETE'])
def deleteEntityRoute():
    entityId = request.args.get('id')

    # Get the MongoDB collection
    collection = mongo.db['your_collection']

    try:
        # Find the entity by custom_id
        existing_entity = collection.find_one({'id': entityId})

        if not existing_entity:
            return jsonify({'message': f'Entity with ID {entityId} not found'}), 404
        
        entityObjectId = existing_entity['_id']

        collection.delete_one({'_id': entityObjectId})

        existing_entity.pop('_id',None)

        return jsonify({'message': f'Entity with ID {entityId} deleted', 'data': existing_entity})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Error occurred during delete'}), 500

CORS(app.app)

if __name__ == '__main__':
    app.run(port=5000)
