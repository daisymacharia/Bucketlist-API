# from flask_api import FlaskAPI
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os.path
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from instance.config import app_config

# from inspect import getsourcefile

# current_path = os.path.abspath(getsourcefile(lambda: 0))
# current_dir = os.path.dirname(current_path)
# parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
#
# sys.path.insert(0, parent_dir)
from app.views import *



# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object('instance.config')
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py', silent=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    api = Api(app)
    api.add_resource(UserRegister, '/api/v1.0/auth/register',
                     endpoint='user_registration')

    return app
