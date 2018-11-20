from flask import current_app, Blueprint, render_template, redirect, request, url_for, jsonify
import os
import pprint
from bson.objectid import ObjectId
from flask import current_app as app
import json
from thetopcut.views.Category import CategoryView

category_ui = Blueprint('category_ui', __name__, url_prefix='/category')
categorys = CategoryView()
@category_ui.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        resp = categorys.get()
        result =  resp.get_json()
        return render_template('category.html', categorys=result)

@category_ui.route('/post', methods=["POST"])
def post():
    resp = categorys.post()
    print('\n\n\n\n')
    if bool(resp):
        return redirect(url_for('category_ui.index'))
        










