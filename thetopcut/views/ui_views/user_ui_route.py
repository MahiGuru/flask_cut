from flask import current_app, Blueprint, render_template, redirect, request, url_for, jsonify
import os
import pprint
from bson.objectid import ObjectId
from flask import current_app as app
import json
from thetopcut.views.UserAPI import UserAPI

user_ui = Blueprint('user_ui', __name__, url_prefix='/user')

user_api = UserAPI()

@user_ui.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        print('\n\n\n\n') 
        result = user_api.get()
        return render_template('user.html', users=result.get_json())

@user_ui.route('/user', methods=["POST"])
def post():
    resp = user_api.post()
    print('\n\n\n\n')
    if bool(resp):
        return redirect(url_for('user_ui.index'))
        










