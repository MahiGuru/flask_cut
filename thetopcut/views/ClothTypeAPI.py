from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_clothType
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, allowed_file, upload_file, moved_file
from thetopcut.models.ClothTypeModel import ClothTypeModel


class ClothTypeAPI(MethodView):

    def __init__(self):
        print("in init")

    def get(self, clothType_id=None):
        myArr = []
        print(clothType_id)
        if clothType_id is None:
            for record in col_clothType.find():
                record['_id'] = str(record['_id'])
                myArr.append(record)
        else:
            for record in col_clothType.find({"_id": ObjectId(clothType_id)}):
                record['_id'] = str(record['_id'])
                myArr.append(record)

        pprint.pprint(myArr)
        return jsonify(myArr)
    def post(self):
        print(os.getcwd())
        upload_folder = os.path.join(os.path.dirname(__file__), '../'+app.config['UPLOAD_FOLDER'])
        #if request.method == "POST":
        print('\n\n\n\n')
        print(request.files)
        if 'images' not in request.files:
            return ''
        clothType_folder = os.path.join(upload_folder, 'clothTypes')
        '' if os.path.exists(clothType_folder) else os.makedirs(clothType_folder)

        fileNamesArr = upload_file(request.files.getlist("images"), clothType_folder, 'ct')
        checkExists = alreadyExists(col_clothType, request.form['type'])
        if checkExists:
            print("Ooops you entered with same name")
        else:
            # record = request.get_data()
            # print(record)
            categoryIds = []
            categoryIds.append(request.form['category'])
            clothType = ClothTypeModel(request.form['type'], request.form['desc'], categoryIds, fileNamesArr)
            clothType_document = clothType.to_document()
            pprint.pprint(clothType.to_document())
             
            insertedId = col_clothType.insert_one(clothType_document).inserted_id
            moved_file(fileNamesArr, clothType_folder, str(insertedId))
        return jsonify(str(insertedId))

    def delete(self, clothType_id=None):
        if clothType_id is not None:
            deleteId = col_clothType.remove({'_id': ObjectId(clothType_id)})
        return jsonify(deleteId)

    def put(self, clothType_id=None):
        if clothType_id is None:
            record = request.get_json()
            result = col_clothType.update({'_id': record['id']}, {'$set': record['data']})
        else:
            result = col_clothType.update({'_id': ObjectId(clothType_id)}, {'$set': record['data']})
        
        return jsonify(result)