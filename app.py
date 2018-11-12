import os

from flask import Flask, redirect, render_template, request, url_for, session
from pymodm import MongoModel, connect, fields
from pymongo.write_concern import WriteConcern
from bson.objectid import ObjectId

from models import Category, FrontViewType

app = Flask(__name__)
# Connect to MongoDB and call the connection "my-app".
# connect("mongodb://192.168.99.100:27017/flaskCut", alias="flask-cut-db")
connect("mongodb://localhost:27017/flaskCut", alias="flask-cut-db")


@app.route('/')
def todo():
    _categorys = Category.objects.all()
    _frontTypes = FrontViewType.objects.all()

    categorys = [item for item in _categorys]
    frontTypes = [item for item in _frontTypes]

    return render_template('types.html', categorys=categorys, frontTypes=frontTypes)


@app.route('/frontviewtype', methods=['POST'])
def frontviewtype():
    category_id = ObjectId(request.form['category'])
    FrontViewType(
        name=request.form['name'],
        description=request.form['description'],
        category=category_id
    ).save(force_insert=True)
    # return redirect(url_for('todo'))
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2500)
