from flask import current_app, Blueprint, render_template, redirect, request, url_for, jsonify
import os
import pprint
from bson.objectid import ObjectId
from flask import current_app as app
import json
from thetopcut.views.BackViewTypeAPI import BackViewTypeAPI
from thetopcut.views.CategoryAPI import CategoryAPI

backview_ui = Blueprint('backview_ui', __name__, url_prefix='/backview')
backview = BackViewTypeAPI()
categorysAPI = CategoryAPI()
@backview_ui.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        front_resp = backview.get()
        backViewResult =  front_resp.get_json()
        cat_resp = categorysAPI.get()
        categorys =  cat_resp.get_json()
        
        return render_template('backview.html', categorys=categorys, backViews=backViewResult)

@backview_ui.route('/post', methods=["POST"])
def post():
    resp = backview.post()
    print('\n\n\n\n')
    if bool(resp):
        return redirect(url_for('backview_ui.index'))
        










