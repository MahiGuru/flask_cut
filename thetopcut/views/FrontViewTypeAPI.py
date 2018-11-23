from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_frontViewType
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, moved_file, upload_images
from thetopcut.models.FrontViewModel import FrontViewModel

from thetopcut.utils.get_collection import get_records
from thetopcut.utils.delete_collection import delete_record
from thetopcut.utils.modify_collection import modify_record

class FrontViewTypeAPI(MethodView):

    def get(self, frontview_id=None):
        return get_records(col_frontViewType, frontview_id)

    def post(self):
        """ below code will move all the images to uploads/category folder with 'cat' prefix """
        upload_files = upload_images(request.files, 'category', 'fvt')
        record = request.form
        """ Values assign to Category Model """
        model_record = FrontViewModel(record['type'], record['desc'], record['category'], upload_files['fileArr'])
        """ Model converts to document like json object """
        record_document = model_record.to_document()
        """ Below line will insert record and get objectID """
        insertedId = col_frontViewType.insert_one(record_document).inserted_id
        """ Below line does files move from one place to another """
        moved_file(upload_files['fileArr'], upload_files['folder'], str(insertedId)) 

        return jsonify(str(insertedId)) 

    def delete(self, frontview_id=None):
        print(frontview_id)
        if frontview_id is not None:
            deleteId = col_frontViewType.remove({'_id': ObjectId(frontview_id)})
        print(deleteId)
        return jsonify(deleteId)

    def put(self, frontview_id=None):
        if frontview_id is None:
            record = request.get_json()
            result = col_frontViewType.update({'_id': record['id']}, {'$set': record['data']})
        else:
            result = col_frontViewType.update({'_id': ObjectId(frontview_id)}, {'$set': record['data']})
        
        return jsonify(result)