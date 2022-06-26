"""
My Service

Describe what your service does here
"""

from audioop import add
import os
import sys
import logging
from flask import jsonify, request, url_for, abort
from .utils import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import CustomerModel, AddressModel, DataValidationError

# Import Flask application
from . import app

BASE_URL = "/customers"

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
# CREATE NEW CUSTOMER
######################################################################
@app.route(f"{BASE_URL}", methods=["POST"])
def create_customers():
    """
    Creates a Customer
    This endpoint will create a Customer based the data in the body that is posted
    """
    app.logger.info("Request to create a customer")
    check_content_type("application/json")
    customer = CustomerModel()
    customer.deserialize(request.get_json())
    customer.create()
    message = customer.serialize()
    location_url = url_for("create_customers", customer_id=customer.customer_id, _external=True)
    app.logger.info("Customer with ID [%s] created.", customer.customer_id)    

    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}

######################################################################
# CREATE NEW ADDRESS
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
######################################################################
@app.route(f"{BASE_URL}/<int:customer_id>/addresses", methods=["POST"])
def create_address(customer_id):
    """
    Creates an Address
    This endpoint will create an Address based the data in the body that is posted
    """
    app.logger.info("Request to create an address")
    check_content_type("application/json")
    address = AddressModel()
    address.deserialize(request.get_json())
    address.create()
    message = address.serialize()
    location_url = url_for("create_address", customer_id=customer_id, address_id=address.address_id, _external=True)
    app.logger.info("Address with ID [%s] created.", address.address_id)

    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}

######################################################################
# DELETE A CUSTOMER
######################################################################
@app.route(f"{BASE_URL}/<int:customer_id>", methods=["DELETE"])
def delete_customers(customer_id):
    """
    Delete a Customer

    This endpoint will delete a Customer based on the id specified in the path
    """
    app.logger.info("Request to delete customer with id: %s", customer_id)
    customer = CustomerModel.find(customer_id)
    if customer:
        customer.delete()

    app.logger.info("Customer with ID [%s] delete complete.", customer_id)
    return "", status.HTTP_204_NO_CONTENT

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    CustomerModel.init_db(app)
    AddressModel.init_db(app)


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )
