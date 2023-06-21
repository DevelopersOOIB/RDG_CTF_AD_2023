from flask import Flask, Blueprint
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from elasticsearch import Elasticsearch

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
elasticsearch = Elasticsearch(app.config['ELASTICSEARCH_URL']) \
    if app.config['ELASTICSEARCH_URL'] else None

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from app import routes, models
