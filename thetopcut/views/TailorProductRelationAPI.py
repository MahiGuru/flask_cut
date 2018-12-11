from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_tailorProductRelation
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.models.TailorRelationModel import TailorProductRelationModel

from thetopcut.database.get_events import get_records
from thetopcut.database.delete_events import delete_record
from thetopcut.database.update_events import modify_record


class TailorProductRelationAPI(MethodView):

    def get(self, _id=None):
        return get_records(col_tailorProductRelation, _id)
        
    def post(self):        
        record = request.json if request.content_type == 'application/json' else request.form
        """ Values assign to Category Model """
        pprint.pprint(record)
        #userid=[], productid=[], designerid=[], tailorid=[]
        model_record = TailorProductRelationModel(
            record['user'], 
            record['product'],
            record['tailor'],
        )
        """ Model converts to document like json object """
        record_document = model_record.to_document()
        """ Below line will insert record and get objectID """
        insertedId = col_tailorProductRelation.insert_one(record_document).inserted_id

        return jsonify(str(insertedId))    

    def delete(self, _id=None):
        if _id is None:
            return "Please provide valid id"
        return delete_record(col_tailorProductRelation, _id)

    def put(self, _id=None):
        if _id is None:
            return "Please provide valid id"
        record = request.get_json()
        return modify_record(col_tailorProductRelation, _id, record['data'])