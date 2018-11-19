from flask import current_app, Blueprint, render_template, redirect, request, url_for, jsonify
import os
import pprint
from thetopcut.db import db
from bson.objectid import ObjectId
from flask import current_app as app
import json
from thetopcut.views.categorys import CategoryAPI
from thetopcut.views.frontViewTypes import FrontViewTypeAPI
from thetopcut.views.backViewTypes import BackViewTypeAPI

groups = Blueprint('groups', __name__, url_prefix='/group')

def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    groups.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET'])
    groups.add_url_rule(url, view_func=view_func, methods=['POST',])
    groups.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

register_api(CategoryAPI, 'category_api', '/categorys/', pk='category_id')
register_api(FrontViewTypeAPI, 'frontviewtype_api', '/frontview/', pk='frontview_id')
register_api(BackViewTypeAPI, 'backviewtype_api', '/backview/', pk='frontview_id')
