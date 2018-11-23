from flask import jsonify, request
from bson.objectid import ObjectId

def delete_record(collection, id):
    deleteId = collection.remove({'_id': ObjectId(id)})
    return jsonify(deleteId)

