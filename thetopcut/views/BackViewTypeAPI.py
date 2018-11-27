from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_backViewType
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, moved_file, upload_images
from thetopcut.models.BackViewModel import BackViewModel

from thetopcut.database.get_events import get_records
from thetopcut.database.delete_events import delete_record
from thetopcut.database.update_events import modify_record

class BackViewTypeAPI(MethodView): 

   
    def get(self, _id=None):
        return get_records(col_backViewType, _id, 'categoryId')

    def post(self):        
        """ below code will move all the images to uploads/category folder with 'fvt' prefix """
        upload_files = upload_images(request.files, 'backViewTypes', 'bvt')
        record = request.json if request.content_type == 'application/json' else request.form
        """ Values assign to Category Model """ 
        recordCat= ObjectId(record['category'])
        model_record = BackViewModel(record['type'], record['desc'], record['category'], upload_files['fileArr'])
        """ Model converts to document like json object """
        record_document = model_record.to_document()
        """ Below line will insert record and get objectID """
        insertedId = col_backViewType.insert_one(record_document).inserted_id
        """ Below line does files move from one place to another """
        if len(upload_files['fileArr']) > 0:
           moved_file(upload_files['fileArr'], upload_files['folder'], str(insertedId)) 

        return jsonify(str(insertedId))

    def delete(self, _id=None):
        if _id is None:
            return "Please provide valid id"
        return delete_record(col_backViewType, _id)

    def put(self, _id=None):
        if _id is None:
            return "Please provide valid id"
        record = request.get_json()
        return modify_record(col_backViewType, _id, record['data'])