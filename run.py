from flask import Flask

from .bucketlist.app import create_app
import os

app = Flask(__name__)
config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
