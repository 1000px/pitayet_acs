from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from serv.api import api as api_blueprint
    CORS(api_blueprint)
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")
    from serv.page import page as page_blueprint
    app.register_blueprint(page_blueprint, url_prefix="/page")

    return app
  