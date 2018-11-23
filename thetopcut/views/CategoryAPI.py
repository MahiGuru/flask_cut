from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_category
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, moved_file, upload_images
from thetopcut.models.CategoryModel import CategoryModel
from thetopcut.utils.get_collection import get_records
from thetopcut.utils.delete_collection import delete_record
from thetopcut.utils.modify_collection import modify_record

class CategoryAPI(MethodView):

    def get(self, category_id=None):
        return get_records(col_category, category_id)

    def post(self):
        """ below code will move all the images to uploads/category folder with 'cat' prefix """
        upload_files = upload_images(request.files, 'category', 'cat')
        record = request.form
        """ Values assign to Category Model """
        model_record = CategoryModel(record['type'], record['desc'], upload_files['fileArr'])
        """ Model converts to document like json object """
        record_document = model_record.to_document()
        """ Below line will insert record and get objectID """
        insertedId = col_category.insert_one(record_document).inserted_id
        """ Below line does files move from one place to another """
        moved_file(upload_files['fileArr'], upload_files['folder'], str(insertedId)) 

        return jsonify(str(insertedId))

    def delete(self, category_id=None):
        if category_id is None:
            return "Please provide valid id"
        return delete_record(col_category, category_id)

    def put(self, category_id=None):
        if category_id is None:
            return "Please provide valid id"
        record = request.get_json()
        return modify_record(col_category, category_id, record['data'])
