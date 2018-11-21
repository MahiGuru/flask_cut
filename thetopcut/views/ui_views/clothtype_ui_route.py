from flask import current_app, Blueprint, render_template, redirect, request, url_for, jsonify
import os
import pprint
from bson.objectid import ObjectId
from flask import current_app as app
import json
from thetopcut.views.ClothTypeAPI import ClothTypeAPI
from thetopcut.views.CategoryAPI import CategoryAPI

clothtype_ui = Blueprint('clothtype_ui', __name__, url_prefix='/clothtype')
clothType = ClothTypeAPI()
categorysAPI = CategoryAPI()
@clothtype_ui.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        front_resp = clothType.get()
        clothTypeResult =  front_resp.get_json()
        cat_resp = categorysAPI.get()
        categorys =  cat_resp.get_json()
        
        return render_template('clothtype.html', categorys=categorys, clothTypes=clothTypeResult)

@clothtype_ui.route('/post', methods=["POST"])
def post():
    resp = clothType.post()
    print('\n\n\n\n')
    if bool(resp):
        return redirect(url_for('clothtype_ui.index'))
        










