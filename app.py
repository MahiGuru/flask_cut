import os

from flask import Flask, redirect, render_template, request, url_for, session
from pymodm import MongoModel, connect, fields
from pymongo.write_concern import WriteConcern
from bson.objectid import ObjectId

from models import Category, FrontViewType

app = Flask(__name__)
# Connect to MongoDB and call the connection "my-app".
# connect("mongodb://192.168.99.100:27017/flaskCut", alias="flask-cut-db")
connect("mongodb://mongodb:27017/flaskCut", alias="flask-cut-db")


@app.route('/')
def todo():
    return render_template('index.html')


@app.route('/category', methods=['POST', 'GET'])
def category():
    # Category(
    #     name=request.form['name'],
    #     description=request.form['description']
    # ).save(force_insert=True)
    Category(
        name='Electronics',
        description='All electronic products'
    ).save(force_insert=True)
    _categorys = Category.objects.all()
    categorys = [item for item in _categorys]
    print(_categorys)
    # return redirect(url_for('todo'))
    return render_template('category.html', categorys=categorys)

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
