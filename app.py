import logging
import os
from importlib import util as importing

from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from api.RomanAPI import roman_api
from persistence.Db import db
from wire_flask.Config import get_config
from wire_flask.Logging import setup_logging
from wire_flask.Metrics import init_metrics
from wire_flask.StatusApi import status_api
from wire_flask.VersionApi import version_api, get_version

logger = setup_logging(__name__,
                       level=logging.DEBUG,
                       json_logging=os.getenv('JSON_LOGGING', 'false').lower() == 'true')


def load_configuration(app):
    config_file = 'local_config'
    if importing.find_spec(config_file):
        app.config.from_object(config_file)


def configure_apis(app):
    # Set up Swagger and API
    authorizations = {
        'bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }

    logger.debug("Creating API.")
    api = Api(app, authorizations=authorizations)

    logger.debug("Creating namespaces.")
    api.add_namespace(roman_api, path='/')
    api.add_namespace(version_api, path='/')
    api.add_namespace(status_api, path='/')


def configure_metrics(app):
    logger.debug("Initialize metrics")
    init_metrics(app, get_version(), 'anthe')


def configure_database(app, config):
    # connect to databas4e
    app.config['SQLALCHEMY_DATABASE_URI'] \
        = f'postgresql+psycopg2://{config.postgres_user}:{config.postgres_password}@{config.postgres_url}/' \
          f'{config.postgres_db}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    return Migrate(app, db)


# Create app
app = Flask(__name__)
# fix for https swagger - see https://github.com/python-restx/flask-restx/issues/58
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)

with app.app_context():
    # load app configuration
    load_configuration(app)
    # add db access
    migrate = configure_database(app, get_config())
    # configure APIs
    configure_apis(app)
    # configure prometheus metrics
    configure_metrics(app)

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
