from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_productRelation
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, upload_images, moved_file
from thetopcut.models.UserModel import UserModel

from thetopcut.database.get_events import get_records
from thetopcut.database.delete_events import delete_record
from thetopcut.database.update_events import modify_record


class ProductRelationAPI(MethodView):

    def get(self, _id=None):
        return get_records(col_productRelation, _id)
        
    def post(self):        
        record = request.json if request.content_type == 'application/json' else request.form
        """ Values assign to Category Model """
        pprint.pprint(record)
        #userid=[], productid=[], designerid=[], tailorid=[]
        model_record = UserModel(
            record['user'], 
            record['product'], 
            record['designer'], 
            record['tailor'],
        )
        """ Model converts to document like json object """
        record_document = model_record.to_document()
        """ Below line will insert record and get objectID """
        insertedId = col_productRelation.insert_one(record_document).inserted_id

        return jsonify(str(insertedId))    

    def delete(self, _id=None):
        if _id is None:
            return "Please provide valid id"
        return delete_record(col_productRelation, _id)

    def put(self, _id=None):
        if _id is None:
            return "Please provide valid id"
        record = request.get_json()
        return modify_record(col_productRelation, _id, record['data'])