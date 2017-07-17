# from flask_api import FlaskAPI
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask import url_for, redirect

import os.path
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from instance.config import app_config
from app.views import *

# initialize sql-alchemy
db = SQLAlchemy()

template = {
    "produces": ["application/json"],
    "consumes": ["application/json"],
    "operationId": "getmyData",
    "content-type": "application/json"
}


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    Swagger(app, template=template)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py', silent=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    @app.route("/")
    def index():
        url = url_for("flasgger.apidocs")
        return redirect(url, code=302)

    api = Api(app)
    api.add_resource(UserRegister, '/api/v1.0/auth/register',
                     endpoint='user_registration')
    api.add_resource(UserLogin, '/api/v1.0/auth/login',
                     endpoint='user_login')
    api.add_resource(CreateBucketlist, '/api/v1.0/bucketlists/',
                     methods=['POST', 'GET'],
                     endpoint='bucketlists')
    api.add_resource(CreateBucketlist, '/api/v1.0/bucketlists/<int:id>/',
                     methods=['PUT', 'GET', 'DELETE'],
                     endpoint='bucketlist')
    api.add_resource(BucketlistItems, '/api/v1.0/bucketlists/<int:id>/items/',
                     methods=['POST', 'GET'],
                     endpoint='bucketlist_items')
    api.add_resource(BucketlistItems,
                     '/api/v1.0/bucketlists/<int:id>/items/<int:item_id>',
                     methods=['PUT', 'GET', 'DELETE'],
                     endpoint='items')

    return app
