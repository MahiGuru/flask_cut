from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_frontViewType
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, moved_file, upload_images
from thetopcut.models.FrontViewModel import FrontViewModel

from thetopcut.database.get_events import get_records
from thetopcut.database.delete_events import delete_record
from thetopcut.database.update_events import modify_record

class FrontViewTypeAPI(MethodView):

    def get(self, _id=None):
        pipeline = [
            {
                "$lookup": {
                    "from": "categorys",
                    "localField": "_id",
                    "foreignField": 'categoryId',
                    "as": "categorys"
                }
            },
            { "$unwind": { "path": "$categorys", "preserveNullAndEmptyArrays": True } },
            {"$group": {"_id": "$_id", 'categoryId' :  {"$first":'$categoryId'}, 'categorys' : {"$first":'$categorys'}}}
        ]
        cursor = col_frontViewType.aggregate(pipeline)
        pprint.pprint(list(cursor))
        # return jsonify([])
        return get_records(col_frontViewType, _id, 'categoryId')

    def post(self):
        """ below code will move all the images to uploads/category folder with 'fvt' prefix """
        upload_files = upload_images(request.files, 'frontViewTypes', 'fvt')
        record = request.json if request.content_type == 'application/json' else request.form
        """ Values assign to Category Model """
        pprint.pprint(record)
        recordCat= ObjectId(record['category'])
        model_record = FrontViewModel(record['type'], record['desc'], recordCat, upload_files['fileArr'])
        """ Model converts to document like json object """
        record_document = model_record.to_document()
        """ Below line will insert record and get objectID """
        insertedId = col_frontViewType.insert_one(record_document).inserted_id
        """ Below line does files move from one place to another """
        if len(upload_files['fileArr']) > 0:
           moved_file(upload_files['fileArr'], upload_files['folder'], str(insertedId)) 
        print(insertedId, '\n\n\n\n\n')
        return jsonify(str(insertedId))

    def delete(self, _id=None):
        if _id is None:
            return "Please provide valid id"
        return delete_record(col_frontViewType, _id)

    def put(self, _id=None):
        if _id is None:
            return "Please provide valid id"
        record = request.get_json()
        return modify_record(col_frontViewType, _id, record['data'])