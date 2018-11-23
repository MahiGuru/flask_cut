from flask import jsonify, request
from bson.objectid import ObjectId

def get_records(collection, id):
    myArr = []
    findObj = {"_id": ObjectId(id)} if id is not None else {}
    for record in collection.find(findObj):
        record['_id'] = str(record['_id'])
        myArr.append(record)

    return jsonify(myArr)
