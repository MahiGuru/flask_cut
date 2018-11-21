from flask import current_app, Blueprint, render_template, redirect, request, url_for, jsonify
import os
import pprint
from bson.objectid import ObjectId
from flask import current_app as app
import json
from thetopcut.views.ProductAPI import ProductAPI
from thetopcut.views.CategoryAPI import CategoryAPI
from thetopcut.views.BackViewTypeAPI import BackViewTypeAPI
from thetopcut.views.FrontViewTypeAPI import FrontViewTypeAPI
from thetopcut.views.BodyTypeAPI import BodyTypeAPI
from thetopcut.views.ClothTypeAPI import ClothTypeAPI
from thetopcut.views.OccassionTypeAPI import OccassionTypeAPI

product_ui = Blueprint('product_ui', __name__, url_prefix='/product')

product = ProductAPI()
category = CategoryAPI()
frontView = FrontViewTypeAPI()
backView = BackViewTypeAPI()
bodyType = BodyTypeAPI()
clothType = ClothTypeAPI()
occassionType = OccassionTypeAPI()

@product_ui.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        products = product.get()
        categorys = category.get()
        frontViews = frontView.get()
        backViews = backView.get()
        bodyTypes = bodyType.get()
        clothTypes = clothType.get()
        occassionTypes = occassionType.get()
        
        return render_template('product.html', 
        categorys=categorys.get_json(), 
        products=products.get_json(),
        frontTypes= frontViews.get_json(),
        backTypes= backViews.get_json(),
        bodyTypes= bodyTypes.get_json(),
        clothTypes= clothTypes.get_json(),
        occassionTypes= occassionTypes.get_json()
        )

@product_ui.route('/post', methods=["POST"])
def post():
    resp = product.post()
    print('\n\n\n\n')
    if bool(resp):
        return redirect(url_for('product_ui.index'))
        










