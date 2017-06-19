from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
import os
from instance.config import app_config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['testing'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app
