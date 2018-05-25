from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler
import os
import logging


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
migrate = Migrate()


db.init_app(app)
migrate.init_app(app, db)


if not app.debug:

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/stageopdracht.log',
                                       maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('App startup')
    app.jinja_env.globals.update


from app import models, routes, errors
