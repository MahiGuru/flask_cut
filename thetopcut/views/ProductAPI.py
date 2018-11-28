from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_products
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, upload_images, moved_file
from thetopcut.models.ProductModel import ProductModel

from thetopcut.database.get_events import get_records, get_all_records
from thetopcut.database.delete_events import delete_record
from thetopcut.database.update_events import modify_record
import re

def splitToArrWithObjectId(str_val):
    str_list = []
    if str_val is not None:
        split_str = re.split(',', str_val)
        for str_val in split_str:
            str_list.append(ObjectId(str_val))        
    return str_list

class ProductAPI(MethodView):

    def get(self, _id=None):
        # return get_records(col_products, _id, ['categorys', 'designerId', 'frontTypes', 'backTypes', 
        # 'occassionTypes', 'clothTypes', 'bodyTypes'])
        return get_all_records(col_products)
        
    def post(self):        
        """ below code will move all the images to uploads/category folder with 'fvt' prefix """
        upload_files = upload_images(request.files, 'products', 'pds')
        record = request.json if request.content_type == 'application/json' else request.form
        """ Values assign to Category Model and also check the keys"""
        pprint.pprint(record)
        name = record['name'] if 'name' in record else ''
        desc = record['desc'] if 'desc' in record else ''
        category_objId= splitToArrWithObjectId(record['category'] if 'category' in record else None)
        designer_objId= splitToArrWithObjectId(record['designer'] if 'designer' in record else None)
        fronttype_objId= splitToArrWithObjectId(record['fronttype'] if 'fronttype' in record else None)
        backType_objId= splitToArrWithObjectId(record['backType'] if 'backType' in record else None)
        occassionType_objId= splitToArrWithObjectId(record['occassionType'] if 'occassionType' in record else None)
        clothType_objId= splitToArrWithObjectId(record['clothType'] if 'clothType' in record else None)
        bodyType_objId= splitToArrWithObjectId(record['bodyType'] if 'bodyType' in record else None)        

        model_record = ProductModel(
            name, 
            desc, 
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
        insertedId = col_products.insert_one(record_document).inserted_id
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