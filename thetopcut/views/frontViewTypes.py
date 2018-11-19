from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.db import db
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, allowed_file, upload_file, moved_file

class FrontViewTypeAPI(MethodView):

    def get(self, frontview_id):
        myArr = []
        print(frontview_id)
        for record in db.frontViewType.find():
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
        frontViewType_folder = os.path.join(upload_folder, 'frontViewTypes')
        '' if os.path.exists(frontViewType_folder) else os.makedirs(frontViewType_folder)

        fileNamesArr = upload_file(request.files.getlist("images"), frontViewType_folder, 'fvt')
        checkExists = alreadyExists(db.frontViewType, request.form['title'])
        if checkExists:
            print("Ooops title already taken")
        else:
            record = request.get_json()
            # category = {
            #     'title': request.form['title'],
            #     'desc': request.form['desc'],
            #     'img': fileNamesArr
            # }
            insertedId = db.frontViewType.insert_one(record).inserted_id
            moved_file(fileNamesArr, frontViewType_folder, str(insertedId))
        return jsonify(str(insertedId))

    def delete(self, frontview_id):
        deleteId = db.frontViewType.remove({'_id': ObjectId(frontview_id)})
        return jsonify(deleteId)

    def put(self, frontview_id):
        record = request.get_json()
        print(record)
        print(frontview_id)
        result = db.frontViewType.update({'_id': ObjectId(frontview_id)}, {'$set': record['data']})
        return jsonify(result)