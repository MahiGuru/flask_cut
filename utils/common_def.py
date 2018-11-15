from flask import Flask, request,flash, redirect
import os
import datetime
import shutil
from datetime import datetime
from werkzeug.utils import secure_filename



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