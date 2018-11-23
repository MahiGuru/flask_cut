from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_occassionType
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, upload_file, moved_file
from thetopcut.models.OccassionTypeModel import OccassionTypeModel


class OccassionTypeAPI(MethodView):

    def __init__(self):
        print("in init")

    def get(self, occassion_id=None):
        myArr = []
        print(occassion_id)
        if occassion_id is None:
            for record in col_occassionType.find():
                record['_id'] = str(record['_id'])
                myArr.append(record)
        else:
            for record in col_occassionType.find({"_id": ObjectId(occassion_id)}):
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
        occassionType_folder = os.path.join(upload_folder, 'occassionTypes')
        '' if os.path.exists(occassionType_folder) else os.makedirs(occassionType_folder)

        fileNamesArr = upload_file(request.files.getlist("images"), occassionType_folder, 'ot')
        checkExists = alreadyExists(col_occassionType, request.form['type'])
        if checkExists:
            print("Ooops you entered with same name")
        else:
            # record = request.get_data()
            # print(record)
            categoryIds = []
            categoryIds.append(request.form['category'])
            occassionTypes = OccassionTypeModel(request.form['type'], request.form['desc'], categoryIds, fileNamesArr)
            occassionTypes_document = occassionTypes.to_document()
            pprint.pprint(occassionTypes.to_document())
             
            insertedId = col_occassionType.insert_one(occassionTypes_document).inserted_id
            moved_file(fileNamesArr, occassionType_folder, str(insertedId))
        return jsonify(str(insertedId))

    def delete(self, occassion_id=None):
        if occassion_id is not None:
            deleteId = col_occassionType.remove({'_id': ObjectId(occassion_id)})
        return jsonify(deleteId)

    def put(self, occassion_id=None):
        if occassion_id is None:
            record = request.get_json()
            result = col_occassionType.update({'_id': record['id']}, {'$set': record['data']})
        else:
            result = col_occassionType.update({'_id': ObjectId(occassion_id)}, {'$set': record['data']})
        
        return jsonify(result)