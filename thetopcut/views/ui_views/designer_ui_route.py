from flask import current_app, Blueprint, render_template, redirect, request, url_for, jsonify
import os
import pprint
from bson.objectid import ObjectId
from flask import current_app as app
import json
from thetopcut.views.DesignerAPI import DesignerAPI

designer_ui = Blueprint('designer_ui', __name__, url_prefix='/designer')

designer = DesignerAPI()

@designer_ui.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        result = designer.get()
        return render_template('designer.html', designers=result.get_json())

@designer_ui.route('/designer', methods=["POST"])
def post():
    resp = designer.post()
    print('\n\n\n\n')
    if bool(resp):
        return redirect(url_for('designer_ui.index'))
        
