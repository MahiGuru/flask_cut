from flask import Flask, request,flash, redirect
import os

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
