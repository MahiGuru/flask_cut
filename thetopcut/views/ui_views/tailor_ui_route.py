from flask import current_app, Blueprint, render_template, redirect, request, url_for, jsonify
import os
import pprint
from bson.objectid import ObjectId
from flask import current_app as app
import json
from thetopcut.views.TailorAPI import TailorAPI

tailor_ui = Blueprint('tailor_ui', __name__, url_prefix='/tailor')

tailor = TailorAPI()

@tailor_ui.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        result = tailor.get()
        return render_template('tailor.html', tailors=result.get_json())

@tailor_ui.route('/tailor', methods=["POST"])
def post():
    resp = tailor.post()
    print('\n\n\n\n')
    if bool(resp):
        return redirect(url_for('tailor_ui.index'))
        
