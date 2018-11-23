from flask import Flask, request,flash, redirect
import os
import datetime
import shutil
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app as app


def upload_images(files, folder, prefix):
        """    Below line will create uploads folder(e.g /categorys) """
        upload_folder = os.path.join(os.path.dirname(__file__), '../'+app.config['UPLOAD_FOLDER'])
        
        """    Below line will create folder(e.g /categorys) """
        category_folder = os.path.join(upload_folder, folder)

        """ Below line will check if folder("category") exists or not """
        '' if os.path.exists(category_folder) else os.makedirs(category_folder)
        
        """     request.files loop here
                push every image object into filesArr
        """
        filesArr = []
        for img in files:
                filesArr.extend(files.getlist(img))
                
        """     file_save method accepts all image objects as "list" and returns fileNames as array.
                params expects folder name("like category_folder" and prefix)
        """
        fileNamesArr = file_save(filesArr, category_folder, prefix)

        """     file_save method accepts all image objects as "list" and returns fileNames as array.
                params expects folder name("like category_folder" and prefix)
        """
        return dict(folder = category_folder, fileArr = fileNamesArr)

def alreadyExists(collection, title):
    print(collection.find({'title': { "$in": [title]}}).count())
    if collection.find({'title': { "$in": [title]}}).count() > 0:
        return True
    else:
        return False

def upload_file(imgArr, folderName, prefix):
    fileNamesArr = []
    print("\n\n\n\n", "UPLOAD METHOD>>>>>")
    for index, filer in enumerate(imgArr):
        datetimestr = "{:%d%m%Y_%H%M%p}".format(datetime.now())
        filename = secure_filename(str(index)+'_'+prefix+'_'+datetimestr+'.'+filer.filename.rsplit('.', 1)[1])
        fileNamesArr.append(filename)
        isAllowedFile = '.' in filer.filename and filer.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        if filer and isAllowedFile:
            filer.save(os.path.join(folderName, filename))
    return fileNamesArr

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def file_save(imgArr, folderName, prefix):
    fileNamesArr = []
    print("\n\n\n\n", "UPLOAD METHOD>>>>>")
    for index, filer in enumerate(imgArr):
        datetimestr = "{:%d%m%Y_%H%M%p}".format(datetime.now())
        filename = secure_filename(str(index)+'_'+prefix+'_'+datetimestr+'.'+filer.filename.rsplit('.', 1)[1])
        fileNamesArr.append(filename)
        isAllowedFile = '.' in filer.filename and filer.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        if filer and isAllowedFile:
            filer.save(os.path.join(folderName, filename))
    return fileNamesArr

def moved_file(files, folderName, objectId):
    os.makedirs(os.path.join(folderName, objectId))
    for index, filer in enumerate(files):
        shutil.move(os.path.join(folderName, filer), os.path.join(folderName+'/'+objectId, filer))