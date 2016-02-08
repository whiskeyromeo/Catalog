import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from .config import config_by_name

db = SQLAlchemy()

import models


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)

    # Register the auth package
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .catalog import catalog as catalog_blueprint
    app.register_blueprint(catalog_blueprint, url_prefix='/catalog')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
