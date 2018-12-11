import os

from flask import Flask, send_from_directory, redirect, url_for
import pprint

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('../config/config.py')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass 
    # from thetopcut.database.db import db
    # print('\n\n\n\n')
    # print(db.category.find())
    from thetopcut.apis.api import api
    from thetopcut.views.ui_views.category_ui_route import category_ui
    from thetopcut.views.ui_views.frontview_ui_route import frontview_ui
    from thetopcut.views.ui_views.backview_ui_route import backview_ui
    from thetopcut.views.ui_views.bodytype_ui_route import bodytype_ui
    from thetopcut.views.ui_views.clothtype_ui_route import clothtype_ui
    from thetopcut.views.ui_views.occassiontype_ui_route import occassiontype_ui
    from thetopcut.views.ui_views.product_ui_route import product_ui
    from thetopcut.views.ui_views.user_ui_route import user_ui
    from thetopcut.views.ui_views.tailor_ui_route import tailor_ui
    from thetopcut.views.ui_views.designer_ui_route import designer_ui
    # from thetopcut.groups_api import groups
    app.register_blueprint(api)
    app.register_blueprint(category_ui)
    app.register_blueprint(frontview_ui)
    app.register_blueprint(backview_ui)
    app.register_blueprint(bodytype_ui)
    app.register_blueprint(clothtype_ui)
    app.register_blueprint(occassiontype_ui)
    app.register_blueprint(product_ui)
    app.register_blueprint(user_ui)
    app.register_blueprint(tailor_ui)
    app.register_blueprint(designer_ui)
    
    # IMAGE Display Route @ UI
    @app.route('/')  
    def reroute():
        return redirect(url_for('category_ui.index'))
     # IMAGE Display Route @ UI
    @app.route('/<path:filename>')  
    def send_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER']+'/', filename)
    

    return app