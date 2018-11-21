from flask import current_app, Blueprint, render_template, redirect, request, url_for, jsonify
import os
import pprint
from bson.objectid import ObjectId
from flask import current_app as app
import json
from thetopcut.views.BodyTypeAPI import BodyTypeAPI
from thetopcut.views.CategoryAPI import CategoryAPI

bodytype_ui = Blueprint('bodytype_ui', __name__, url_prefix='/bodytype')
bodytypes = BodyTypeAPI()
categorysAPI = CategoryAPI()
@bodytype_ui.route('/', methods=["GET"])
def index():
    if request.method == "GET":
       bodytype_resp = bodytypes.get()
       bodytypeResult =  bodytype_resp.get_json()
       cat_resp = categorysAPI.get()
       categorys =  cat_resp.get_json()
        
       return render_template('bodytype.html', categorys=categorys, bodytypes=bodytypeResult)

@bodytype_ui.route('/post', methods=["POST"])
def post():
    resp = bodytypes.post()
    print('\n\n\n\n')
    if bool(resp):
        return redirect(url_for('bodytype_ui.index'))
        










