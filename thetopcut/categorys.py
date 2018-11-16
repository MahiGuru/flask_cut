from flask import current_app, Blueprint, render_template, redirect, render_template, request, url_for, session, flash, send_from_directory
import os
import pprint
from thetopcut.db import db
from datetime import datetime
from werkzeug.utils import secure_filename
from pathlib import Path
import shutil
from flask import current_app as app


def alreadyExists(collection, title):
    print(collection.find({'title': { "$in": [title]}}).count())
    if collection.find({'title': { "$in": [title]}}).count() > 0:
        return True
    else:
        return False

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def upload_file(imgArr, folderName, prefix):
    fileNamesArr = []
    for index, filer in enumerate(imgArr):
        datetimestr = "{:%d%m%Y_%H%M%p}".format(datetime.now())
        filename = secure_filename(str(index)+'_'+prefix+'_'+datetimestr+'.'+filer.filename.rsplit('.', 1)[1])
        fileNamesArr.append(filename)
        if filer and allowed_file(filer.filename):
            filer.save(os.path.join(folderName, filename))
    return fileNamesArr

def moved_file(files, folderName, objectId):
    os.makedirs(os.path.join(folderName, objectId))
    for index, filer in enumerate(files):
        shutil.move(os.path.join(folderName, filer), os.path.join(folderName+'/'+objectId, filer))

categorys = Blueprint('categorys', __name__, url_prefix='/category')

@categorys.route('/index', methods=["GET", "POST"])
def index():
    print(os.getcwd())
    upload_folder = os.path.join(os.path.dirname(__file__), app.config['UPLOAD_FOLDER'])
    if request.method == "POST":
        if 'images' not in request.files:
            return redirect(request.url)
        # category_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'category')
        category_folder = os.path.join(upload_folder, 'category')
        print(category_folder)
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