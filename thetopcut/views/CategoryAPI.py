from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_category
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, allowed_file, upload_file, moved_file
from thetopcut.models.CategoryModel import CategoryModel

class CategoryAPI(MethodView):

    def get(self, category_id=None):

        myArr = []
        print(category_id)
        if category_id is None:
            for record in col_category.find():
                record['_id'] = str(record['_id'])
                myArr.append(record)
        else:
            for record in col_category.find({"_id": ObjectId(category_id)}):
                record['_id'] = str(record['_id'])
                myArr.append(record)

        pprint.pprint(myArr)
        return jsonify(myArr)
    def post(self):
        print(os.getcwd())
        upload_folder = os.path.join(os.path.dirname(__file__), '../'+app.config['UPLOAD_FOLDER'])
        
        if 'images' not in request.files:
            return ''
        category_folder = os.path.join(upload_folder, 'category')
        '' if os.path.exists(category_folder) else os.makedirs(category_folder)

        fileNamesArr = upload_file(request.files.getlist("images"), category_folder, 'cat')
        checkExists = alreadyExists(col_category, request.form['type'])        
        if checkExists:
            print("Ooops you entered with same name")
        else:
            record = request.form
            print(record)
            category_arr = CategoryModel(record['type'], record['desc'], fileNamesArr)
            category = category_arr.to_document()
            insertedId = col_category.insert_one(category).inserted_id
            moved_file(fileNamesArr, category_folder, str(insertedId)) 
        return jsonify(str(insertedId))

    def delete(self, category_id=None):
        print(category_id)
        if category_id is not None:
            deleteId = col_category.remove({'_id': ObjectId(category_id)})
        print(deleteId)
        return jsonify(deleteId)

    def put(self, category_id=None):
        if category_id is None:
            record = request.get_json()
            result = col_category.update({'_id': record['id']}, {'$set': record['data']})
        else:
            result = col_category.update({'_id': ObjectId(category_id)}, {'$set': record['data']})
        
        return jsonify(result)
