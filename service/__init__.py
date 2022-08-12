"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import sys
# import logging
from flask import Flask
from service import config
from .utils import log_handlers
from flask_restx import Api

# Create Flask application
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(config)

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Customers REST API Service',
          description='This is a customers service.',
          default='customers',
          default_label='Customers management',
          doc='/apidocs',
          prefix='/api'
          )

# Dependencies require we import the routes AFTER the Flask app is created
# from service import routes, models
from service import routes  # pylint: disable=wrong-import-position, wrong-import-order
from .utils import error_handlers, cli_commands  # pylint: disable=wrong-import-position

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    routes.init_db()  # make our SQLAlchemy tables
except Exception as error:
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

app.logger.info("Service initialized!")
