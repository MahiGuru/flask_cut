from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_backViewType
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, allowed_file, upload_file, moved_file
from thetopcut.models.BackViewModel import BackViewModel


class BackViewTypeAPI(MethodView):

    def __init__(self):
        print("in init")

    def get(self, backview_id=None):
        myArr = []
        print(backview_id)
        if backview_id is None:
            for record in col_backViewType.find():
                record['_id'] = str(record['_id'])
                myArr.append(record)
        else:
            for record in col_backViewType.find({"_id": ObjectId(backview_id)}):
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
        backview_folder = os.path.join(upload_folder, 'backViewTypes')
        '' if os.path.exists(backview_folder) else os.makedirs(backview_folder)

        fileNamesArr = upload_file(request.files.getlist("images"), backview_folder, 'fvt')
        checkExists = alreadyExists(col_backViewType, request.form['type'])
        if checkExists:
            print("Ooops you entered with same name")
        else:
            # record = request.get_data()
            # print(record)
            categoryIds = []
            categoryIds.append(request.form['category'])
            backviews = BackViewModel(request.form['type'], request.form['desc'], categoryIds, fileNamesArr)
            backviews_document = backviews.to_document()
            pprint.pprint(backviews.to_document())
             
            insertedId = col_backViewType.insert_one(backviews_document).inserted_id
            moved_file(fileNamesArr, backview_folder, str(insertedId))
        return jsonify(str(insertedId))

    def delete(self, backview_id=None):
        if backview_id is not None:
            deleteId = col_backViewType.remove({'_id': ObjectId(backview_id)})
        return jsonify(deleteId)

    def put(self, backview_id=None):
        if backview_id is None:
            record = request.get_json()
            result = col_backViewType.update({'_id': record['id']}, {'$set': record['data']})
        else:
            result = col_backViewType.update({'_id': ObjectId(backview_id)}, {'$set': record['data']})
        
        return jsonify(result)