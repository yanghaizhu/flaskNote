# init to create flask application.
from  flask import Flask
# import views, also run views.
from .viewsHome import *

def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint=homeBlueprint)
    return app
