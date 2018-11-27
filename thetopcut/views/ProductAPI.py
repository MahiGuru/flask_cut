from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_products
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, upload_images, moved_file
from thetopcut.models.ProductModel import ProductModel

from thetopcut.database.get_events import get_records
from thetopcut.database.delete_events import delete_record
from thetopcut.database.update_events import modify_record
import re

def splitToArrWithObjectId(str):
    split_str = re.split(',', str)
    str_list = []
    for str in split_str:
        str_list.append(ObjectId(str))
    return str_list
def propertyExists(obj, property):
    myval =  obj[property] if obj is not None else []
    print('\n\n\n\n', myval, '\n\n\n\n')
    return myval

class ProductAPI(MethodView):

    def get(self, _id=None):
        return get_records(col_products, _id)
        
    def post(self):        
        """ below code will move all the images to uploads/category folder with 'fvt' prefix """
        upload_files = upload_images(request.files, 'products', 'pds')
        record = request.json if request.content_type == 'application/json' else request.form
        """ Values assign to Category Model """
        pprint.pprint(record)
        category_objId= splitToArrWithObjectId(propertyExists(record, 'category'))
        designer_objId= record['designer']
        fronttype_objId= splitToArrWithObjectId(record['fronttype'])
        backType_objId= splitToArrWithObjectId(record['backType'])
        occassionType_objId= splitToArrWithObjectId(record['occassionType'])
        clothType_objId= splitToArrWithObjectId(record['clothType'])
        bodyType_objId= splitToArrWithObjectId(record['bodyType'])

        model_record = ProductModel(
            record['name'], 
            record['desc'], 
            category_objId, 
            designer_objId, 
            fronttype_objId, 
            backType_objId, 
            occassionType_objId, 
            clothType_objId,
            bodyType_objId,  
            upload_files['fileArr']
        )
        """ Model converts to document like json object """
        record_document = model_record.to_document()
        """ Below line will insert record and get objectID """
        insertedId = list()
        #insertedId = col_products.insert_one(record_document).inserted_id
        """ Below line does files move from one place to another """
        if len(upload_files['fileArr']) > 0:
           moved_file(upload_files['fileArr'], upload_files['folder'], str(insertedId)) 

        return jsonify(str(insertedId))    

    def delete(self, _id=None):
        if _id is None:
            return "Please provide valid id"
        return delete_record(col_products, _id)

    def put(self, _id=None):
        if _id is None:
            return "Please provide valid id"
        record = request.get_json()
        return modify_record(col_products, _id, record['data'])