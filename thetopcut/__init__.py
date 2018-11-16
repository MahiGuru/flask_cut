import os

from flask import Flask, send_from_directory
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
    # from thetopcut.db import db
    # print('\n\n\n\n')
    # print(db.category.find())
    
    from thetopcut.categorys import categorys
    app.register_blueprint(categorys)
    
    # IMAGE Display Route @ UI
    @app.route('/<path:filename>')  
    def send_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER']+'/', filename)


    return app