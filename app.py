import os

from flask import Flask, redirect, render_template, request, url_for, session, flash
from bson.objectid import ObjectId
from pymongo import MongoClient
import pprint
from datetime import datetime
from utils.common_def import alreadyExists, allowed_file
from werkzeug.utils import secure_filename


app = Flask(__name__)

#image info
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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

def upload_file(filer,name):
    print(filer)
    if filer.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if filer and allowed_file(filer.filename):
        # d = datetime.date.today()
        # filename = secure_filename('_cat_'+id+'_'+str(datetime.now().strftime('%Y_%m_%d')) +'.'+filer.filename.rsplit('.', 1)[1])
        filer.save(os.path.join(app.config['UPLOAD_FOLDER'], name))

@app.route('/category', methods=['POST', 'GET'])
def category():
    if request.method == "POST":
        category = {
            'title': request.form['title'],
            'desc': request.form['desc']
        }
        insertedId= ''
        if 'images' not in request.files:
            flash('No file part')
            return redirect(request.url)
        checkExists = alreadyExists(categorys, request.form['title'])
        if checkExists:
            print("Ooops you entered with same name")
        else: 
            print("still called")
            insertedId = categorys.insert_one(category).inserted_id
            print("\n\n\n\n")
            print(insertedId)
        for index, filer in enumerate(request.files.getlist("images")):
            print(str(insertedId))
            filename = str(index)+'_cat_'+str(insertedId)+'.'+filer.filename.rsplit('.', 1)[1]
            print(filename)
            upload_file(filer, filename)
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
