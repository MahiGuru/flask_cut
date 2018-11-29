from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_products
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, upload_images, moved_file
from thetopcut.models.ProductModel import ProductModel

import json
from thetopcut.database.get_events import get_all_records
import re



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class ProductWithTypesAPI(MethodView):

    def get(self, _id=None):
        findObj = {"_id": ObjectId(_id)} if _id is not None else {}
        pipeline = [
                { "$match": findObj },
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
        cursor = col_products.aggregate(pipeline)
        myresult = []
        for result in cursor:
            myresult.append(result)
        res = JSONEncoder().encode(myresult)
        return jsonify(json.loads(res))
