from flask import current_app, Blueprint, render_template, redirect, request, url_for, jsonify
import os
import pprint
from thetopcut.database.db import db
from bson.objectid import ObjectId
from flask import current_app as app
import json
from thetopcut.views.CategoryAPI import CategoryAPI
from thetopcut.views.FrontViewTypeAPI import FrontViewTypeAPI
from thetopcut.views.BackViewTypeAPI import BackViewTypeAPI
from thetopcut.views.BodyTypeAPI import BodyTypeAPI
from thetopcut.views.ClothTypeAPI import ClothTypeAPI
from thetopcut.views.OccassionTypeAPI import OccassionTypeAPI
from thetopcut.views.ProductAPI import ProductAPI
from thetopcut.views.UserAPI import UserAPI
from thetopcut.views.TailorAPI import TailorAPI
from thetopcut.views.DesignerAPI import DesignerAPI
from thetopcut.views.ProductRelationAPI import ProductRelationAPI

api = Blueprint('api', __name__, url_prefix='/api')

def register_api(view, endpoint, url, pk='_id', pk_type='string'):
    view_func = view.as_view(endpoint)
    api.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET'])
    api.add_url_rule(url, view_func=view_func, methods=['POST',])
    api.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func, methods=['GET', 'PUT', 'DELETE'])

register_api(CategoryAPI, 'category_api', '/categorys/')
register_api(FrontViewTypeAPI, 'frontviewtype_api', '/frontview/')
register_api(BackViewTypeAPI, 'backviewtype_api', '/backview/')
register_api(BodyTypeAPI, 'bodytype_api', '/bodytype/')
register_api(ClothTypeAPI, 'clothtype_api', '/clothtype/')
register_api(OccassionTypeAPI, 'occassiontype_api', '/occassiontype/')
register_api(ProductAPI, 'products_api', '/products/')
register_api(UserAPI, 'users_api', '/users/')
register_api(TailorAPI, 'tailor_api', '/tailors/')
register_api(DesignerAPI, 'designer_api', '/designers/')
register_api(ProductRelationAPI, 'product_realtion_api', '/productrelations/')
