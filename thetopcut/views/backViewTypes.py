from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import db
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, allowed_file, upload_file, moved_file

class BackViewTypeAPI(MethodView):

    def get(self, backview_id):
        myArr = []
        print(backview_id)
        for record in db.backViewTypes.find():
            record['_id'] = str(record['_id'])
            myArr.append(record)
        pprint.pprint(myArr)
        return jsonify(myArr)
    def post(self):
        print(os.getcwd())
        upload_folder = os.path.join(os.path.dirname(__file__), '../'+app.config['UPLOAD_FOLDER'])
        #if request.method == "POST":
        if 'images' not in request.files:
            return ''
        backViewType_folder = os.path.join(upload_folder, 'backViewTypes')
        '' if os.path.exists(backViewType_folder) else os.makedirs(backViewType_folder)

        fileNamesArr = upload_file(request.files.getlist("images"), backViewType_folder, 'fvt')
        checkExists = alreadyExists(db.backViewTypes, request.form['title'])
        if checkExists:
            print("Ooops you entered with same name")
        else:
            backviewType = {
                'title': request.form['title'],
                'desc': request.form['desc'],
                'img': fileNamesArr
            }
            insertedId = db.backViewTypes.insert_one(backviewType).inserted_id
            moved_file(fileNamesArr, backViewType_folder, str(insertedId))
        return jsonify(str(insertedId))

    def delete(self, backview_id):
        deleteId = db.backViewTypes.remove({'_id': ObjectId(backview_id)})
        return jsonify(deleteId)

    def put(self, backview_id):
        record = request.get_json()
        result = db.backViewTypes.update({'_id': ObjectId(backview_id)}, {'$set': record['data']})
        return jsonify(result)