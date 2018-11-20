from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_frontViewType
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, allowed_file, upload_file, moved_file
from thetopcut.models.FrontViewModel import FrontViewModel


class FrontViewTypeAPI(MethodView):

    def __init__(self):
        print("in init")

    def get(self, frontview_id=None):
        myArr = []
        print(frontview_id)
        if frontview_id is None:
            for record in col_frontViewType.find():
                record['_id'] = str(record['_id'])
                myArr.append(record)
        else:
            for record in col_frontViewType.find({"_id": ObjectId(frontview_id)}):
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
        frontview_folder = os.path.join(upload_folder, 'frontViewTypes')
        '' if os.path.exists(frontview_folder) else os.makedirs(frontview_folder)

        fileNamesArr = upload_file(request.files.getlist("images"), frontview_folder, 'fvt')
        checkExists = alreadyExists(col_frontViewType, request.form['type'])
        if checkExists:
            print("Ooops you entered with same name")
        else:
            # record = request.get_data()
            # print(record)
            categoryIds = []
            categoryIds.append(request.form['category'])
            frontviews = FrontViewModel(request.form['type'], request.form['desc'], categoryIds, fileNamesArr)
            frontviews_document = frontviews.to_document()
            pprint.pprint(frontviews.to_document())
             
            insertedId = col_frontViewType.insert_one(frontviews_document).inserted_id
            moved_file(fileNamesArr, frontview_folder, str(insertedId))
        return jsonify(str(insertedId))

    def delete(self, frontview_id=None):
        print(frontview_id)
        if frontview_id is not None:
            deleteId = col_frontViewType.remove({'_id': ObjectId(frontview_id)})
        print(deleteId)
        return jsonify(deleteId)

    def put(self, frontview_id=None):
        if frontview_id is None:
            record = request.get_json()
            result = col_frontViewType.update({'_id': record['id']}, {'$set': record['data']})
        else:
            result = col_frontViewType.update({'_id': ObjectId(frontview_id)}, {'$set': record['data']})
        
        return jsonify(result)