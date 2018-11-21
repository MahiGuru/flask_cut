from flask import current_app, Blueprint, render_template, redirect, request, url_for, jsonify
import os
import pprint
from bson.objectid import ObjectId
from flask import current_app as app
import json
from thetopcut.views.OccassionTypeAPI import OccassionTypeAPI
from thetopcut.views.CategoryAPI import CategoryAPI

occassiontype_ui = Blueprint('occassiontype_ui', __name__, url_prefix='/occassiontype')
occassiontypes = OccassionTypeAPI()
categorysAPI = CategoryAPI()
@occassiontype_ui.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        front_resp = occassiontypes.get()
        occassiontypeResult =  front_resp.get_json()
        cat_resp = categorysAPI.get()
        categorys =  cat_resp.get_json()
        
        return render_template('occassionType.html', categorys=categorys, occassionTypes=occassiontypeResult)

@occassiontype_ui.route('/post', methods=["POST"])
def post():
    resp = occassiontypes.post()
    print('\n\n\n\n')
    if bool(resp):
        return redirect(url_for('occassiontype_ui.index'))
        










