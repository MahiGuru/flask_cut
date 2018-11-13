import os

from flask import Flask, redirect, render_template, request, url_for, session, flash
from bson.objectid import ObjectId
from pymongo import MongoClient
import pprint
from datetime import datetime
from werkzeug.utils import secure_filename
import pathlib

app = Flask(__name__)

from utils.common_def import alreadyExists, allowed_file
#image info
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['CATEGORY'] = app.config['UPLOAD_FOLDER']+'/'+'categorys'


app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# for DOCKER CONFIG
# connect("mongodb://192.168.99.100:27017/flaskCut", alias="flask-cut-db")
# connect("mongodb://mongo:27017/flaskCut", alias="flask-cut-db")

client = MongoClient('mongodb://localhost:27017/')
# client = MongoClient('mongodb://mongodb:27017/')
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
    if request.method == "POST":
        
        insertedId= ''
        if 'images' not in request.files:
            flash('No file part')
            return redirect(request.url)
        checkExists = alreadyExists(categorys, request.form['title'])
        if checkExists:
            print("Ooops you entered with same name")
        else:
            file111 = [file.filename for file in request.files.getlist("images")]
            category = {
                'title': request.form['title'],
                'desc': request.form['desc']
            }
            insertedId = categorys.insert_one(category).inserted_id
            
        # os.makedirs(os.path.join(app.config['UPLOAD_FOLDER']+'/'+str(insertedId)))    
        # pathlib.Path(os.path.join(app.config['UPLOAD_FOLDER']+'/'+str(insertedId))).mkdir(parents=True, exist_ok=True)
        fileNamesArr = []    
        for index, filer in enumerate(request.files.getlist("images")):
            filename = str(index)+'_cat_'+str(insertedId)+'.'+filer.filename.rsplit('.', 1)[1]
            fileNamesArr.append(filename)
            if filer and allowed_file(filer.filename):
                filer.save(os.path.join(app.config['CATEGORY']), filename)
        categorys.find_one_and_update({'_id': insertedId}, {'$inc': {'count': 1}, '$set': {'files': fileNamesArr}})

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
    # _categorys = Category.objects.all()
    # categorys = [item for item in _categorys]
    # _frontTypes = FrontViewType.objects.all()
    # frontTypes = [item for item in _frontTypes]
    # return redirect(url_for('todo'))
    categorys = []
    frontTypes = []
    return render_template('frontTypes.html', categorys=categorys, frontTypes=frontTypes)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
