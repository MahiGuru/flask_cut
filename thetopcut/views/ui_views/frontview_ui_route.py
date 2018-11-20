from flask import current_app, Blueprint, render_template, redirect, request, url_for, jsonify
import os
import pprint
from bson.objectid import ObjectId
from flask import current_app as app
import json
from thetopcut.views.FrontViewTypeAPI import FrontViewTypeAPI
from thetopcut.views.CategoryAPI import CategoryAPI

frontview_ui = Blueprint('frontview_ui', __name__, url_prefix='/frontview')
frontviews = FrontViewTypeAPI()
categorysAPI = CategoryAPI()
@frontview_ui.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        front_resp = frontviews.get()
        frontViewResult =  front_resp.get_json()
        cat_resp = categorysAPI.get()
        categorys =  cat_resp.get_json()
        
        return render_template('frontview.html', categorys=categorys, frontViews=frontViewResult)

@frontview_ui.route('/post', methods=["POST"])
def post():
    resp = frontviews.post()
    print('\n\n\n\n')
    if bool(resp):
        return redirect(url_for('frontview_ui.index'))
        










