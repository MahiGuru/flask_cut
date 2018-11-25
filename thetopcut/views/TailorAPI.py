from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_tailors
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, upload_images, moved_file
from thetopcut.models.TailorModel import TailorModel

from thetopcut.database.get_events import get_records
from thetopcut.database.delete_events import delete_record
from thetopcut.database.update_events import modify_record


class TailorAPI(MethodView):

    def get(self, _id=None):
        return get_records(col_tailors, _id)
        
    def post(self):        
        """ below code will move all the images to uploads/category folder with 'fvt' prefix """
        upload_files = upload_images(request.files, 'tailors', 'tailor')
        record = request.json if request.content_type == 'application/json' else request.form
        """ Values assign to Category Model """
        pprint.pprint(record)
        #userid, name, desc, contactNumber, alternateNumber, address, 
        # landmark, pincode, locationObj, img
        model_record = TailorModel(
            record['user'], 
            record['name'], 
            record['desc'], 
            record['contactNumber'], 
            record['alternateNumber'], 
            record['address'],
            record['landmark'],
            record['pincode'],
            record['locationObj'],
            upload_files['fileArr']
        )
        """ Model converts to document like json object """
        record_document = model_record.to_document()
        """ Below line will insert record and get objectID """
        insertedId = col_tailors.insert_one(record_document).inserted_id
        """ Below line does files move from one place to another """
        if len(upload_files['fileArr']) > 0:
           moved_file(upload_files['fileArr'], upload_files['folder'], str(insertedId)) 

        return jsonify(str(insertedId))    

    def delete(self, _id=None):
        if _id is None:
            return "Please provide valid id"
        return delete_record(col_tailors, _id)

    def put(self, _id=None):
        if _id is None:
            return "Please provide valid id"
        record = request.get_json()
        return modify_record(col_tailors, _id, record['data'])