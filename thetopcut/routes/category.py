
import os
import pprint
from flask import Flask, redirect, render_template, request, url_for, session, flash, View
from werkzeug.utils import secure_filename
from utils.common_def import alreadyExists, allowed_file


class CategoryView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == "POST":
            insertedId = ''
            if 'images' not in request.files:
                flash('No file part')
                return redirect(request.url)
            checkExists = alreadyExists(categorys, request.form['title'])
            if checkExists:
                print("Ooops you entered with same name")
            else:
                file111 = [
                    file.filename for file in request.files.getlist("images")]
                category = {
                    'title': request.form['title'],
                    'desc': request.form['desc']
                }
                insertedId = categorys.insert_one(category).inserted_id

            os.makedirs(os.path.join(
                app.config['UPLOAD_FOLDER']+'/'+str(insertedId)))
            # pathlib.Path(os.path.join(app.config['UPLOAD_FOLDER']+'/'+str(insertedId))).mkdir(parents=True, exist_ok=True)
            fileNamesArr = []

            for index, filer in enumerate(request.files.getlist("images")):
                id = str(insertedId)
                filename = secure_filename(
                    str(index)+'_cat_'+id + '.'+filer.filename.rsplit('.', 1)[1])
                fileNamesArr.append(filename)
                if filer and allowed_file(filer.filename):
                    filer.save(os.path.join(
                        app.config['UPLOAD_FOLDER']+'/'+id, filename))

            categorys.find_one_and_update(
                {'_id': insertedId}, {'$inc': {'count': 1}, '$set': {'files': fileNamesArr}})
            return redirect(url_for('category'))

        elif request.method == "GET":
            myArr = []
            for record in categorys.find():
                myArr.append(record)
            pprint.pprint(myArr)
            return render_template('category.html', categorys=myArr)
