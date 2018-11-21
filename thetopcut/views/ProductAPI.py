from flask import jsonify, request
from flask.views import View, MethodView
import pprint
from thetopcut.database.db import col_products
import os
from flask import current_app as app
from bson.objectid import ObjectId
from thetopcut.utils.common_def import alreadyExists, allowed_file, upload_file, moved_file
from thetopcut.models.ProductModel import ProductModel


class ProductAPI(MethodView):

    def __init__(self):
        print("in init")

    def get(self, product_id=None):
        myArr = []
        print(product_id)
        if product_id is None:
            for record in col_products.find():
                record['_id'] = str(record['_id'])
                myArr.append(record)
        else:
            for record in col_products.find({"_id": ObjectId(product_id)}):
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
        products_folder = os.path.join(upload_folder, 'products')
        '' if os.path.exists(products_folder) else os.makedirs(products_folder)

        fileNamesArr = upload_file(request.files.getlist("images"), products_folder, 'pts')
        checkExists = alreadyExists(col_products, request.form['name'])
        if checkExists:
            print("Ooops you entered with same name")
        else:
            record = request.get_json()
            print("GET JSON DATA ")
            pprint.pprint(record)

            product_obj = ProductModel(request.form['name'], request.form['desc'])
            product_obj.designerId = [(request.form['designer'])]
            product_obj.frontTypes = [(request.form['frontType'])]
            product_obj.backTypes = [(request.form['backType'])]
            product_obj.occassionTypes = [(request.form['occassionType'])]
            product_obj.clothTypes = [(request.form['clothType'])]
            product_obj.bodyTypes = [(request.form['bodyType'])]
            product_obj.img = fileNamesArr 
             
            insertedId = col_products.insert_one(product_obj.to_document()).inserted_id
            moved_file(fileNamesArr, products_folder, str(insertedId))
        return jsonify(str(insertedId))

    def delete(self, product_id=None):
        if product_id is not None:
            deleteId = col_products.remove({'_id': ObjectId(product_id)})
        return jsonify(deleteId)

    def put(self, product_id=None):
        if product_id is None:
            record = request.get_json()
            result = col_products.update({'_id': record['id']}, {'$set': record['data']})
        else:
            result = col_products.update({'_id': ObjectId(product_id)}, {'$set': record['data']})
        
        return jsonify(result)