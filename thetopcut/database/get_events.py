from flask import jsonify, request
from bson.objectid import ObjectId
import pprint
from bson import json_util
from bson.json_util import dumps

def get_records(collection, id, relationId = []):
    myArr = []
    findObj = {"_id": ObjectId(id)} if id is not None else {}
    for record in collection.find(findObj):
        record['_id'] = str(record['_id'])
        for key in relationId:
            if key is not None:
                record[key] = str(record[key])

        myArr.append(record)

    return jsonify(myArr)
def get_all_records(collection):
    pipeline = [
            { "$unwind": { "path": "$categorys", "preserveNullAndEmptyArrays": True } },
            {
                "$lookup": {
                    "from": "categorys",
                    "localField": "categorys",
                    "foreignField": '_id',
                    "as": "categorys_obj"
                }
            },
            { "$unwind": { "path": "$categorys_obj", "preserveNullAndEmptyArrays": True } },
            { "$unwind": { "path": "$frontTypes", "preserveNullAndEmptyArrays": True } },
            {
                "$lookup": {
                    "from": "frontTypes",
                    "localField": "frontTypes",
                    "foreignField": '_id',
                    "as": "frontType_obj"
                }
            },
            { "$unwind": { "path": "$frontType_obj", "preserveNullAndEmptyArrays": True } },
            { "$unwind": { "path": "$backTypes", "preserveNullAndEmptyArrays": True } },
            {
                "$lookup": {
                    "from": "backTypes",
                    "localField": "backTypes",
                    "foreignField": '_id',
                    "as": "backType_obj"
                }
            },
            { "$unwind": { "path": "$backType_obj", "preserveNullAndEmptyArrays": True } },
            { "$unwind": { "path": "$occassionTypes", "preserveNullAndEmptyArrays": True } },
            {
                "$lookup": {
                    "from": "occassionTypes",
                    "localField": "occassionTypes",
                    "foreignField": '_id',
                    "as": "occassionType_obj"
                }
            },
            { "$unwind": { "path": "$occassionType_obj", "preserveNullAndEmptyArrays": True } },
            { "$unwind": { "path": "$clothTypes", "preserveNullAndEmptyArrays": True } },
            {
                "$lookup": {
                    "from": "clothTypes",
                    "localField": "clothTypes",
                    "foreignField": '_id',
                    "as": "clothType_obj"
                }
            },
            { "$unwind": { "path": "$clothType_obj", "preserveNullAndEmptyArrays": True } },
            { "$unwind": { "path": "$bodyTypes", "preserveNullAndEmptyArrays": True } },
            {
                "$lookup": {
                    "from": "bodyTypes",
                    "localField": "bodyTypes",
                    "foreignField": '_id',
                    "as": "bodyType_obj"
                }
            },
            { "$unwind": { "path": "$bodyType_obj", "preserveNullAndEmptyArrays": True } },
           {
               "$group": {
                   "_id": "$_id", 
                   "name": {"$first": "$name"},
                   "desc": {"$first": "$desc"},
                    'categorys' : {"$push":'$categorys_obj'},
                    'frontTypes' : {"$push":'$frontType_obj'},
                    'backTypes' : {"$push":'$backType_obj'},
                    'occassionTypes' : {"$push":'$occassionType_obj'},
                    'clothTypes' : {"$push":'$clothType_obj'},
                    'bodyTypes' : {"$push":'$bodyType_obj'}
                
                
                }
            }
        ]
    cursor = collection.aggregate(pipeline)
    for result in cursor: 
        myresult = result 
    return dumps(myresult)
