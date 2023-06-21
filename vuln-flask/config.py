import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'changeme'
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    # Don't use sqlite db in production environment
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    WTF_CSRF_ENABLED = False
    WERKZEUG_DEBUG_PIN = os.environ.get('WERKZEUG_DEBUG_PIN') or 'off'
