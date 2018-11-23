from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_bodyType
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, upload_file, moved_file
from thetopcut.models.BodyTypeModel import BodyTypeModel


class BodyTypeAPI(MethodView):

    def __init__(self):
        print("in init")

    def get(self, bodytype_id=None):
        myArr = []
        if bodytype_id is None:
            for record in col_bodyType.find():
                record['_id'] = str(record['_id'])
                myArr.append(record)
        else:
            for record in col_bodyType.find({"_id": ObjectId(bodytype_id)}):
                record['_id'] = str(record['_id'])
                myArr.append(record)

        return jsonify(myArr)
    def post(self):
        print(os.getcwd())
        upload_folder = os.path.join(os.path.dirname(__file__), '../'+app.config['UPLOAD_FOLDER'])
        print('\n\n\n\n')
        print(request.files)
        if 'images' not in request.files:
            return ''
        bodytype_folder = os.path.join(upload_folder, 'bodyTypes')
        '' if os.path.exists(bodytype_folder) else os.makedirs(bodytype_folder)

        fileNamesArr = upload_file(request.files.getlist("images"), bodytype_folder, 'bt')
        checkExists = alreadyExists(col_bodyType, request.form['type'])
        if checkExists:
            print("Ooops you entered with same name")
        else:
            # record = request.get_data()
            # print(record)
            categoryIds = []
            categoryIds.append(request.form['category'])
            bodytypes = BodyTypeModel(request.form['type'], request.form['desc'], categoryIds, fileNamesArr)
            bodytypes_document = bodytypes.to_document()
             
            insertedId = col_bodyType.insert_one(bodytypes_document).inserted_id
            moved_file(fileNamesArr, bodytype_folder, str(insertedId))
        return jsonify(str(insertedId))

    def delete(self, bodytype_id=None):
        if bodytype_id is not None:
            deleteId = col_bodyType.remove({'_id': ObjectId(bodytype_id)})
        return jsonify(deleteId)

    def put(self, bodytype_id=None):
        if bodytype_id is None:
            record = request.get_json()
            result = col_bodyType.update({'_id': record['id']}, {'$set': record['data']})
        else:
            result = col_bodyType.update({'_id': ObjectId(bodytype_id)}, {'$set': record['data']})
        
        return jsonify(result)