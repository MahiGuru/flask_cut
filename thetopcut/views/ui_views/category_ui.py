from flask import current_app, Blueprint, render_template, redirect, request, url_for, jsonify
import os
import pprint
from thetopcut.db import db
from bson.objectid import ObjectId
from flask import current_app as app
import json
from thetopcut.views.categorys import CategoryAPI

category_ui = Blueprint('category_ui', __name__, url_prefix='/category')

@category_ui.route('/get', methods=["GET", "POST"])
def categorys():
    if request.method == "GET":
        resp = CategoryAPI.get('', '')
        result =  resp.get_json()
        return render_template('category.html', categorys=result)
    elif request.method == "POST":
        resp = CategoryAPI.post('', '')
        if result:
            return redirect(url_for('views.categorys'))
        










