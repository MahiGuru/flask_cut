from flask import jsonify, request
from bson.objectid import ObjectId

def modify_record(collection, id=None, data={}):  
    record = request.get_json()
    result = collection.update({'_id': ObjectId(id)}, {'$set': data})
    return jsonify(result)