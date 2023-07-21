from flask import Flask
from .config import Config
from .extensions import db,migrate,cache
from . import prescriptions
from . import errors
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app=app,db=db)
    register_blueprints(app)
    register_erorrs(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(prescriptions.api.api_blueprint)


def register_erorrs(app: Flask):
    app.register_error_handler(Exception,errors.error_500)
    app.register_error_handler(404,errors.error_404)


#main module
