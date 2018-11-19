from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.db import db
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, allowed_file, upload_file, moved_file


class RatingsAPI(MethodView):

    def get(self, rating_id):
        myArr = []
        print(rating_id)
        for record in db.ratings.find():
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
        checkExists = alreadyExists(db.ratings, request.form['title'])
        if checkExists:
            print("Ooops you entered with same name")
        else:
            rating_obj = {
                'title': request.form['title'],
                'desc': request.form['desc'],
                'img': fileNamesArr
            }
            insertedId = db.ratings.insert_one(rating_obj).inserted_id
            moved_file(fileNamesArr, category_folder, str(insertedId))
        return jsonify(str(insertedId))

    def delete(self, rating_id):
        deleteId = db.ratings.remove({'_id': ObjectId(rating_id)})
        return jsonify(deleteId)

    def put(self, rating_id):
        record = request.get_json()
        result = db.ratings.update({'_id': ObjectId(rating_id)}, {'$set': record['data']})
        return jsonify(result)