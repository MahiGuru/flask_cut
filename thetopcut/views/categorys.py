from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.db import db
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, allowed_file, upload_file, moved_file


class CategoryAPI(MethodView):

    def get(self, category_id):
        myArr = []
        print(category_id)
        for record in db.categorys.find():
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
        category_folder = os.path.join(upload_folder, 'category')
        '' if os.path.exists(category_folder) else os.makedirs(category_folder)

        fileNamesArr = upload_file(request.files.getlist("images"), category_folder, 'cat')
        checkExists = alreadyExists(db.categorys, request.form['title'])
        if checkExists:
            print("Ooops you entered with same name")
        else:
            category = {
                'title': request.form['title'],
                'desc': request.form['desc'],
                'img': fileNamesArr
            }
            insertedId = db.categorys.insert_one(category).inserted_id
            moved_file(fileNamesArr, category_folder, str(insertedId))
        return jsonify(str(insertedId))

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, category_id):
        record = request.get_json()
        print(record)
        print(category_id)
        result = db.categorys.update({'_id': ObjectId(category_id)}, {'$set': record['data']})
        return jsonify(result)