from flask import current_app, Blueprint, render_template, redirect, request, url_for, jsonify
import os
import pprint
from thetopcut.db import db
from bson.objectid import ObjectId
from flask import current_app as app
import json
from .method_views.category import CategoryAPI


categorys = Blueprint('categorys', __name__, url_prefix='/category')

def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    categorys.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    categorys.add_url_rule(url, view_func=view_func, methods=['POST',])
    categorys.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

register_api(CategoryAPI, 'category_api', '/category/', pk='category_id')



@categorys.route('/index', methods=["GET", "POST", "DELETE"])
def index():
    print(os.getcwd())
    upload_folder = os.path.join(os.path.dirname(__file__), app.config['UPLOAD_FOLDER'])
    if request.method == "POST":
        if 'images' not in request.files:
            return redirect(request.url)
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
        return redirect(url_for('categorys.index'))

    elif request.method == "GET":
        myArr = []
        for record in db.categorys.find():
            myArr.append(record)
        pprint.pprint(myArr)
        return render_template('category.html', categorys=myArr)

    elif request.method == "DELETE":
        search = request.get_json()
        deleteId = db.categorys.remove({'_id': ObjectId(search['id'])})
        return jsonify(deleteId)

@categorys.route('/update', methods=["POST"])
def update():
    record = request.get_json()
    print(record)
    result = db.categorys.update({'_id': ObjectId(record['id'])}, {'$set': record['data']})
    # return jsonify(result)
    return redirect(url_for('categorys.index'))










