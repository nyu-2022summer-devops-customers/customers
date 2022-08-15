"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort
from .utils import status  # HTTP Status Codes
import datetime

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from service.models import CustomerModel, AddressModel

# Import Flask application
from . import app

BASE_URL = "/customers"


def abort_when_customer_not_exist(customer_id):
    customer = CustomerModel.find(customer_id)
    if customer is None:
        abort(status.HTTP_400_BAD_REQUEST, f"Addresses with id '{customer_id}' was not found.")

############################################################
# Health Endpoint
############################################################


@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK

######################################################################
# GET INDEX
######################################################################
@app.before_request
def pre_request_logging():
    #Logging statement
    app.logger.info('\t'.join([
        datetime.datetime.today().ctime(),
        request.remote_addr,
        request.method,
        request.url,
        str(request.data),
        ', '.join([': '.join(x) for x in request.headers])])
    )

@app.route("/")
def index():
    """ Root URL response """
    return app.send_static_file("index.html")

    # return (
    #     "Reminder: return some useful information in json format about the service here",
    #     status.HTTP_200_OK,
    # )
    # return (
    #    jsonify(
    #        title="Customer REST Service",
    #        description="This is the customers service",
    #        version="1.0.0",
    #        list_customers=f"GET {BASE_URL}",
    #        create_customers=f"POST {BASE_URL}",
    #        get_a_customer=f"GET {BASE_URL}/<int:customer_id>",
    #        update_a_customer=f"PUT {BASE_URL}/<int:customer_id>",
    #        delete_a_customer=f"DELETE {BASE_URL}/<int:customer_id>",
    #        activate_a_customer=f"PUT {BASE_URL}/<int:customer_id>/activate",
    #        deactivate_a_customer=f"DELETE {BASE_URL}/<int:customer_id>/deactivate",
    #        create_address=f"POST {BASE_URL}/<int:customer_id>/addresses",
    #        get_an_address_of_a_customer=f"GET {BASE_URL}/<int:customer_id>/addresses/<int:address_id>",
    #        list_addresses=f"GET {BASE_URL}/<int:customer_id>/addresses",
    #        update_an_address_of_a_customer=f"PUT {BASE_URL}/<int:customer_id>/addresses/<int:address_id>",
    #        delete_an_address_of_a_customer=f"DELETE {BASE_URL}/<int:customer_id>/addresses/<int:address_id>",
    #        get_customer_list_by_nickname=f"GET {BASE_URL}?nickname=<string:nickname>",
    #        get_customer_list_by_email=f"GET {BASE_URL}?nickname=<string:email>",
    #        get_customer_list_by_name=f"GET {BASE_URL}?firstname=<string:firstname>&lastname=<string:lastname>",
    #        get_customer_list_by_birthday=f"GET {BASE_URL}?birthday=<string:birthday>"
    #    ),
    #    status.HTTP_200_OK
    # )


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
# UPDATE AN ADDRESS OF A CUSTOMER
######################################################################
@app.route(f"{BASE_URL}/<int:customer_id>/addresses/<int:address_id>", methods=["PUT"])
def update_an_address_of_a_customer(customer_id, address_id):
    """
    Update an Address of a Customer
    This endpoint will delete an Address based on the data in the body that is posted
    """
    app.logger.info("Update an Address of a Customer")
    check_content_type("application/json")
    abort_when_customer_not_exist(customer_id=customer_id)
    address = AddressModel()
    address.deserialize(request.get_json())
    address.update()

    found = AddressModel.find_by_customer_and_address_id(customer_id, address_id)
    if found.count() == 0:
        abort(status.HTTP_404_NOT_FOUND, f"Address with id '{address_id}' was not found.")

    address = found[0]
    address.deserialize(request.get_json())
    address.update()

    app.logger.info("Address with ID [%s] updated.", address.address_id)
    return jsonify(address.serialize()), status.HTTP_200_OK


######################################################################
# UPDATE A CUSTOMER
######################################################################
@app.route(f"{BASE_URL}/<int:customer_id>", methods=["PUT"])
def update_a_customer(customer_id):
    """
    Update a Customer

    This endpoint will update a Customer based the body that is posted
    """
    app.logger.info("Request to update customer with id: %s", customer_id)
    check_content_type("application/json")

    customer = CustomerModel.find(customer_id)
    if not customer:
        abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found.")

    customer.deserialize(request.get_json())
    customer.customer_id = customer_id
    customer.update()

    app.logger.info("Customer with ID [%s] updated.", customer.customer_id)
    return jsonify(customer.serialize()), status.HTTP_200_OK


######################################################################
# READ A CUSTOMER BY CUSTOMER_ID
######################################################################
@app.route(f"{BASE_URL}/<int:customer_id>", methods=["GET"])
def get_a_customer(customer_id):
    """
    Retrieve a single Customer

    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request for customer with id: %s", customer_id)
    customer: CustomerModel = CustomerModel.find(customer_id)
    if not customer:
        abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found.")

    app.logger.info("Returning customer: Id %s, Name %s %s", customer.customer_id, customer.first_name, customer.last_name)
    return jsonify(customer.serialize()), status.HTTP_200_OK


######################################################################
# LIST ALL CUSTOMERS
######################################################################
@app.route("/customers", methods=["GET"])
def list_customers():  # noqa: C901
    """List customers"""
    def list_all_customers():
        """Returns all of the Customers"""
        app.logger.info("Request for customer list")
        customers = []
        customers = CustomerModel.all()

        results = [customer.serialize() for customer in customers]
        app.logger.info("Returning %d customers", len(results))
        return jsonify(results), status.HTTP_200_OK

    def list_all_customers_by_nickname(nickname):
        """
        Retrieve a Customer list by nickname
        """
        app.logger.info("Request for customer with nickname: %s", nickname)
        customers = CustomerModel.find_by_nickname(nickname=nickname)
        res = []
        for customer in customers:
            res.append(customer.serialize())
        return jsonify(res), status.HTTP_200_OK

    def list_all_customers_by_email(email):
        """
        Retrieve a Customer list by email
        """
        app.logger.info("Request for customer with email: %s", email)
        customers = CustomerModel.find_by_email(email=email)
        res = []
        for customer in customers:
            res.append(customer.serialize())
        return jsonify(res), status.HTTP_200_OK

    def list_all_customers_by_name(firstname, lastname):
        """
        Retrieve a Customer list by name
        """
        app.logger.info("Request for customer with name: %s %s", firstname, lastname)
        customers = CustomerModel.find_by_name(firstname, lastname)
        res = []
        for customer in customers:
            res.append(customer.serialize())
        return jsonify(res), status.HTTP_200_OK

    def list_all_customers_by_birthday(birthday):
        """
        Retrieve a Customer list by birthday
        """
        app.logger.info("Request for customer with birthday: %s", birthday)
        customers = CustomerModel.find_by_birthday(birthday)
        res = []
        for customer in customers:
            res.append(customer.serialize())
        return jsonify(res), status.HTTP_200_OK

    args = request.args
    nickname = args.get("nickname")
    email = args.get("email")
    firstname = args.get('firstname')
    lastname = args.get('lastname')
    birthday = args.get('birthday')

    if args.get('nickname'):
        return list_all_customers_by_nickname(nickname=nickname)
    elif args.get('email'):
        return list_all_customers_by_email(email=email)
    elif args.get('birthday'):
        return list_all_customers_by_birthday(birthday=birthday)
    elif firstname and lastname:
        return list_all_customers_by_name(firstname, lastname)
    else:
        return list_all_customers()


######################################################################
# ACTIVATE A CUSTOMER
######################################################################
@app.route(f"{BASE_URL}/<int:customer_id>/activate", methods=["PUT"])
def activate_a_customers(customer_id):
    """Activate a customer"""
    app.logger.info("Request to activate customer with id: %s', customer_id")
    # check_content_type("application/json")

    customer = CustomerModel.find(customer_id)
    if not customer:
        abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found.")

    customer.is_active = True
    customer.update()

    app.logger.info(
        "Customer with ID [%s] updated.",
        customer.customer_id
    )
    return jsonify(customer.serialize()), status.HTTP_200_OK


######################################################################
# DEACTIVATE A CUSTOMER
######################################################################
@app.route(f"{BASE_URL}/<int:customer_id>/deactivate", methods=["DELETE"])
def deactivate_a_customer(customer_id):
    """Deactivate a customer"""
    app.logger.info("Request to deactivate customer with id: %s', customer_id")
    # check_content_type("application/json")

    customer = CustomerModel.find(customer_id)
    if not customer:
        abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found.")

    customer.is_active = False
    customer.update()

    app.logger.info("Customer with ID [%s] updated.", customer.customer_id)
    return jsonify(customer.serialize()), status.HTTP_200_OK


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
    abort_when_customer_not_exist(customer_id=customer_id)
    address = AddressModel()
    address.deserialize(request.get_json())
    address.create()
    message = address.serialize()
    location_url = url_for("create_address", customer_id=customer_id) + f"/{address.address_id}"
    app.logger.info("Address with ID [%s] created.", address.address_id)

    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# LIST ALL ADDRESS OF A GIVEN CUSTOMER
######################################################################
@app.route(f"{BASE_URL}/<int:customer_id>/addresses", methods=["GET"])
def list_addresses(customer_id):
    """
    List all Address of a given customer
    This endpoint will create an Address based the data in the body that is posted
    """
    app.logger.info("Request for addresses with customer id: %s", customer_id)
    abort_when_customer_not_exist(customer_id=customer_id)
    addresses = AddressModel.find_by_customer_id(customer_id=customer_id)
    if addresses.count() == 0:
        abort(status.HTTP_404_NOT_FOUND, f"Addresses with id '{customer_id}' was not found.")

    app.logger.info("All address under customer ID [%s].", customer_id)

    res = []
    for addr in addresses:
        res.append(addr.serialize())
    return jsonify(res), status.HTTP_200_OK


######################################################################
# GET AN ADDRESS OF A CUSTOMER
######################################################################
@app.route(f"{BASE_URL}/<int:customer_id>/addresses/<int:address_id>", methods=["GET"])
def get_an_address_of_a_customer(customer_id, address_id):
    """
    Get an Address of a Customer
    This endpoint will create an Address based the data in the body that is posted
    """
    app.logger.info("Get an Address of a Customer")
    abort_when_customer_not_exist(customer_id=customer_id)
    found = AddressModel.find_by_customer_and_address_id(customer_id=customer_id, address_id=address_id)

    if found.count() == 0:
        abort(status.HTTP_404_NOT_FOUND, f"Address '{address_id}' with customer id '{customer_id}' was not found.")
    address = found[0]

    app.logger.info(address.serialize())

    return jsonify(address.serialize()), status.HTTP_200_OK


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
    abort_when_customer_not_exist(customer_id=customer_id)
    customer = CustomerModel.find(customer_id)
    if customer:
        customer.delete()

    app.logger.info("Customer with ID [%s] delete complete.", customer_id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# DELETE AN ADDRESS OF A CUSTOMER
######################################################################
@app.route(f"{BASE_URL}/<int:customer_id>/addresses/<int:address_id>", methods=["DELETE"])
def delete_an_address_of_a_customer(customer_id, address_id):
    """
    Delete an Address of a Customer
    This endpoint will delete an Address based on the data in the body that is posted
    """
    app.logger.info("Delete an Address of a Customer")
    abort_when_customer_not_exist(customer_id=customer_id)
    found = AddressModel.find_by_customer_and_address_id(customer_id=customer_id, address_id=address_id)

    if found.count() == 1:
        address = found[0]
        address.delete()

    app.logger.info(f"Address '{address_id}' with customer id '{customer_id}' delete complete.")

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
