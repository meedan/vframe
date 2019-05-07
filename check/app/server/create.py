import os
import logging
import logging.handlers

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler("flask.log",
    maxBytes=3000000, backupCount=2)
formatter = logging.Formatter(
    '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logging.getLogger().addHandler(logging.StreamHandler())

logging.debug("starting app")

from flask import Flask, Blueprint, jsonify, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from app.models.sql_factory import connection_url

from app.settings import app_cfg as cfg
from app.server.api import api

db = SQLAlchemy()

def create_app(script_info=None):
  """
  functional pattern for creating the flask app
  """
  app = Flask(__name__, static_folder='static', static_url_path='/static')
  app.config['SQLALCHEMY_DATABASE_URI'] = connection_url
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['CELERY_BROKER_URL'] = cfg.CELERY_BROKER_URL
  app.config['CELERY_RESULT_BACKEND'] = cfg.CELERY_RESULT_BACKEND

  db.init_app(app)

  app.register_blueprint(api, url_prefix='/api')

  @app.errorhandler(404)
  def page_not_found(e):
    path = os.path.join(os.path.dirname(__file__), './static', request.path[1:], 'index.html')
    if os.path.exists(path):
      with open(path, "r") as f:
        return f.read(), 200
    return "404", 404

  @app.route('/', methods=['GET'])
  def index():
    return app.send_static_file('index.html')

  @app.shell_context_processor
  def shell_context():
    return { 'app': app, 'db': db }

  return app
