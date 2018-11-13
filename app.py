import os

from flask import Flask, redirect, render_template, request, url_for, session
from pymongo.write_concern import WriteConcern
from bson.objectid import ObjectId
from pymongo import MongoClient
from utils.common_def import alreadyExists

from models import Category, FrontViewType

import pprint


app = Flask(__name__)
# Connect to MongoDB and call the connection "my-app".
# connect("mongodb://192.168.99.100:27017/flaskCut", alias="flask-cut-db")
# connect("mongodb://mongo:27017/flaskCut", alias="flask-cut-db")

client = MongoClient('mongodb://localhost:27017/')
db = client.flaskCut
# listout all collections
# pprint.pprint(db.collection_names(include_system_collections=False))

categorys = db.category
frontViewTypes = db.frontViewType
backViewTypes = db.backViewType


@app.route('/')
def todo():
    return render_template('index.html')

@app.route('/category', methods=['POST', 'GET'])
def category():
    # Category(
    #     name=request.form['name'],
    #     description=request.form['description']
    # ).save(force_insert=True)
    # Category(
    #     name='Electronics',
    #     description='All electronic products'
    # ).save(force_insert=True)
    # _categorys = Category.objects.all()
    if request.method == "POST":
        category = {
            'title': request.form['title'],
            'desc': request.form['desc']
        }
        checkExists = alreadyExists(categorys, request.form['title'])
        print("\n\n\n")

        print(checkExists)

        print("\n\n\n")
        if checkExists:
            print("Ooops you entered with same name")
        else: 
            print("still called")
            categorys.insert_one(category)

        return redirect(url_for('category'))
    elif request.method == "GET":
        myArr = []
        for record in categorys.find():
            myArr.append(record)
        pprint.pprint(myArr)    
        return render_template('category.html', categorys=myArr)

    

@app.route('/frontviewtype', methods=['POST', 'GET'])
def frontviewtype():
    # category_id = ObjectId(request.form['category'])
    # FrontViewType(
    #     name=request.form['name'],
    #     description=request.form['description'],
    #     category=category_id
    # ).save(force_insert=True)
    # return redirect(url_for('todo'))
    _categorys = Category.objects.all()
    categorys = [item for item in _categorys]
    _frontTypes = FrontViewType.objects.all()
    frontTypes = [item for item in _frontTypes]
    # return redirect(url_for('todo'))
    return render_template('frontTypes.html', categorys=categorys, frontTypes=frontTypes)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
