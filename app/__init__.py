from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the views
from app import views

# local import
from config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


# Load the config file
app.config.from_object('config')
