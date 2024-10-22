"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, abort
from .utils import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from service.models import CustomerModel, AddressModel, Gender
from flask_restx import Resource, reqparse, fields

# Import Flask application
from . import app, api
BASE_URL = '/customers'


def abort_when_customer_not_exist(customer_id):
    """ Rise 404 NOT Found if the customer id not exist """
    customer = CustomerModel.find(customer_id)
    if customer is None:
        abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found.")

############################################################
# Health Endpoint
############################################################


@app.route("/health")
def health():
    """ Health Status """
    return jsonify(dict(status="OK")), status.HTTP_200_OK

######################################################################
# GET INDEX
# Configure the Root route before OpenAPI
######################################################################


@app.route("/")
def index():
    """ Root URL response """
    return app.send_static_file("index.html")

############################################################
# Flask-RESTx and OpenAPI Config
############################################################


# Customer
# Define the model so that the docs reflect what can be sent
create_model = api.model('Customer', {
    'password': fields.String(required=True,
                              description='The password of the Customer'),
    'first_name': fields.String(required=True,
                                description='The first_name of the Customer'),
    'last_name': fields.String(required=True,
                               description='The first_name of the Customer'),
    'nickname': fields.String(required=True,
                              description='The nickname of the Customer'),
    'email': fields.String(required=True,
                           description='The email of the Customer'),
    'gender': fields.String(enum=Gender._member_names_, description='The gender of the Customer'),
    'birthday': fields.Date(required=True, description='The day the customer was born'),
    'is_active': fields.Boolean(required=True,
                                description='Is the Customer alive?')
})

customer_model = api.inherit(
    'CustomerModel',
    create_model,
    {
        'customer_id': fields.Integer(readOnly=True,
                                      description='The unique id assigned internally by service'),
    }
)

# Address
# Define the model so that the docs reflect what can be sent
create_address_model = api.model('Address', {
    'customer_id': fields.Integer(required=True,
                                  description='The customer id that this address belongs to'),
    'address': fields.String(required=True,
                             description='The address detail'),
})

address_model = api.inherit(
    'AddressModel',
    create_address_model,
    {
        'address_id': fields.Integer(readOnly=True, description='The unique id assigned internally by service')
    }
)

# query string arguments
customer_args = reqparse.RequestParser()


######################################################################
#  PATH: /customers/{customer_id}
######################################################################
@api.route(f'{BASE_URL}/<int:customer_id>')
@api.param('customer_id', 'The customer identifier')
class CustomerResource(Resource):
    """
    CustomerResource class

    Allows the manipulation of a single Customer
    GET /customers/{customer_id} - Returns a Customer with the id
    PUT /customers/{customer_id} - Update a Customer with the id
    DELETE /customers/{customer_id} -  Deletes a Customer with the id
    """
    # ------------------------------------------------------------------
    # RETRIEVE A CUSTOMER
    # ------------------------------------------------------------------
    @api.doc('get_customers')
    @api.response(404, 'Customer not found')
    @api.marshal_with(customer_model)
    def get(self, customer_id):
        """
        Retrieve a single Customer
        This endpoint will return a Customer based on his/her id
        """
        app.logger.info("Request to Retrieve a customer with id [%s]", customer_id)
        customer = CustomerModel.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))
        return customer.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING CUSTOMER
    # ------------------------------------------------------------------
    @api.doc('update_customers')
    @api.response(404, 'Customer not found')
    @api.response(400, 'The posted Customer data was not valid')
    @api.expect(customer_model)
    @api.marshal_with(customer_model)
    def put(self, customer_id):
        """
        Update a Customer
        This endpoint will update a Customer based the body that is posted
        """
        app.logger.info('Request to Update a customer with id [%s]', customer_id)
        customer = CustomerModel.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        customer.deserialize(data)
        customer.customer_id = customer_id
        customer.update()
        return customer.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A CUSTOMER
    # ------------------------------------------------------------------
    @api.doc('delete_customers')
    @api.response(204, 'Customer deleted')
    def delete(self, customer_id):
        """
        Delete a Customer
        This endpoint will delete a Customer based the id specified in the path
        """
        app.logger.info('Request to Delete a customer with id [%s]', customer_id)
        customer = CustomerModel.find(customer_id)
        if customer:
            customer.delete()
            app.logger.info('Customer with id [%s] was deleted', customer_id)

        return '', status.HTTP_204_NO_CONTENT


@api.route(f'{BASE_URL}', strict_slashes=False)
class CustomerCollection(Resource):
    """
    CustomerCollection class

    Like create, list operations
    """
    # ------------------------------------------------------------------
    # ADD A NEW CUSTOMER
    # ------------------------------------------------------------------
    @api.doc('create_customers')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(customer_model, code=201)
    def post(self):
        """
        Creates a Customer
        This endpoint will create a Pet based the data in the body that is posted
        """
        app.logger.info('Request to Create a Customer')
        customer = CustomerModel()
        app.logger.debug('Payload = %s', api.payload)
        customer.deserialize(api.payload)
        customer.create()
        app.logger.info('Customer with new id [%s] created!', customer.customer_id)
        location_url = api.url_for(CustomerResource, customer_id=customer.customer_id, _external=True)
        return customer.serialize(), status.HTTP_201_CREATED, {'Location': location_url}

    # ------------------------------------------------------------------
    # LIST ALL CUSTOMERS
    # ------------------------------------------------------------------
    @api.doc('list_customers')
    @api.expect(customer_args, validate=True)
    @api.marshal_list_with(customer_model)
    def get(self):

        def list_all_customers():
            """Returns all of the Customers"""
            app.logger.info("Request for customer list")
            customers = []
            customers = CustomerModel.all()

            results = [customer.serialize() for customer in customers]
            app.logger.info("Returning %d customers", len(results))
            return results, status.HTTP_200_OK

        def list_all_customers_by_nickname(nickname):
            """
            Retrieve a Customer list by nickname
            """
            app.logger.info("Request for customer with nickname: %s", nickname)
            customers = CustomerModel.find_by_nickname(nickname=nickname)
            results = [customer.serialize() for customer in customers]
            return results, status.HTTP_200_OK

        def list_all_customers_by_email(email):
            """
            Retrieve a Customer list by email
            """
            app.logger.info("Request for customer with email: %s", email)
            customers = CustomerModel.find_by_email(email=email)
            results = [customer.serialize() for customer in customers]
            return results, status.HTTP_200_OK

        def list_all_customers_by_name(firstname, lastname):
            """
            Retrieve a Customer list by name
            """
            app.logger.info("Request for customer with name: %s %s", firstname, lastname)
            customers = CustomerModel.find_by_name(firstname, lastname)
            results = [customer.serialize() for customer in customers]
            return results, status.HTTP_200_OK

        def list_all_customers_by_birthday(birthday):
            """
            Retrieve a Customer list by birthday
            """
            app.logger.info("Request for customer with birthday: %s %s", birthday)
            customers = CustomerModel.find_by_birthday(birthday)
            results = [customer.serialize() for customer in customers]
            return results, status.HTTP_200_OK

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
#  PATH: /customers/{customer_id}/addresses/{address_id}
######################################################################
@api.route(f'{BASE_URL}/<int:customer_id>/addresses/<int:address_id>')
@api.param('customer_id', 'The customer identifier')
@api.param('address_id', 'The address identifier')
class AddressResource(Resource):
    """
    AddressResource class

    Allows the manipulation of a single Address
    GET /customers/{customer_id}/addresses/{address_id} - Returns a Customer with the id
    PUT /customers/{customer_id}/addresses/{address_id} - Update a Customer with the id
    DELETE /customers/{customer_id}/addresses/{address_id} -  Deletes a Customer with the id
    """

    # ------------------------------------------------------------------
    # GET AN ADDRESS OF A CUSTOMER
    # ------------------------------------------------------------------
    @api.doc('retrieve_customers_address')
    @api.response(404, 'Address not found')
    @api.marshal_with(address_model)
    def get(self, customer_id, address_id):
        """
        Get an Address of a Customer
        This endpoint will create an Address based the data in the body that is posted
        """
        app.logger.info("Get an Address of a Customer ")
        abort_when_customer_not_exist(customer_id=customer_id)
        found = AddressModel.find_by_customer_and_address_id(customer_id=customer_id, address_id=address_id)

        if found.count() == 0:
            abort(status.HTTP_404_NOT_FOUND, "Address with id '{}' was not found.".format(address_id))
        address = found[0]

        app.logger.info("Address [%s] with customer id [%s]] retrieve complete.", address_id, customer_id)
        return address.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN ADDRESS OF A CUSTOMER
    # ------------------------------------------------------------------
    @api.doc('delete_customers_address')
    @api.response(204, 'Address deleted')
    def delete(self, customer_id, address_id):
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
            app.logger.info("Address [%s] with customer id [%s]] delete complete.", address_id, customer_id)
        return "", status.HTTP_204_NO_CONTENT

    # ------------------------------------------------------------------
    # UPDATE AN ADDRESS OF A CUSTOMER
    # ------------------------------------------------------------------
    @api.doc('update_customers_address')
    @api.response(200, 'Address updated')
    @api.response(404, 'Address not found')
    @api.response(400, 'The posted Address data was not valid')
    @api.marshal_with(address_model)
    @api.expect(address_model)
    def put(self, customer_id, address_id):
        """
        Update an Address of a Customer
        This endpoint will delete an Address based on the data in the body that is posted
        """
        app.logger.info("Update an Address of a Customer")
        # check_content_type("application/json")
        abort_when_customer_not_exist(customer_id=customer_id)
        address = AddressModel()
        address.deserialize(request.get_json())
        address.update()

        found = AddressModel.find_by_customer_and_address_id(customer_id, address_id)

        if found.count() == 0:
            abort(status.HTTP_404_NOT_FOUND, "Address with id '{}' was not found.".format(address_id))

        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        address = found[0]
        address.deserialize(data)
        address.address_id = address_id
        address.update()

        app.logger.info("Address with ID [%s] updated.", address.address_id)
        return address.serialize(), status.HTTP_200_OK


@api.route(f'{BASE_URL}/<int:customer_id>/addresses', strict_slashes=False)
@api.param('customer_id', 'The customer identifier')
class AddressCollection(Resource):
    """
    CustomerCollection class

    Like create, list operations
    """
    # ------------------------------------------------------------------
    # ADD A NEW CUSTOMER ADDRESS
    # ------------------------------------------------------------------
    @api.doc('create_customers_address')
    @api.response(404, 'Customer not found')
    @api.response(400, 'The posted Address data was not valid')
    @api.expect(create_address_model)
    @api.marshal_with(address_model, code=201)
    def post(self, customer_id):
        """
        Creates an Address
        This endpoint will create an Address based the data in the body that is posted
        """
        app.logger.info("Request to create an address")
        abort_when_customer_not_exist(customer_id=customer_id)
        address = AddressModel()
        app.logger.debug('Payload = %s', api.payload)
        address.deserialize(api.payload)
        address.create()
        app.logger.info("Address with address_id [%s] is created!", address.address_id)
        location_url = api.url_for(AddressResource, customer_id=customer_id, address_id=address.address_id, _external=True)

        return address.serialize(), status.HTTP_201_CREATED, {"Location": location_url}

    # ------------------------------------------------------------------
    # LIST ALL ADDRESSES
    # ------------------------------------------------------------------
    @api.doc('list_customers')
    @api.response(404, 'Customer not found')
    @api.marshal_list_with(address_model)
    def get(self, customer_id):
        """
        List all Addresses of a given customer
        """
        app.logger.info("Request for addresses with customer id: %s", customer_id)
        abort_when_customer_not_exist(customer_id=customer_id)
        addresses = AddressModel.find_by_customer_id(customer_id=customer_id)

        app.logger.info("Addresses under customer ID [%s] returned.", customer_id)
        results = [address.serialize() for address in addresses]

        return results, status.HTTP_200_OK


######################################################################
#  PATH: /customers/{customer_id}/activate
######################################################################
@api.route(f"{BASE_URL}/<int:customer_id>/activate", methods=["PUT"])
@api.param('customer_id', 'The customer identifier')
class ActivateResource(Resource):
    """ Activate actions on a Customer """
    @api.doc('activate_customer')
    @api.response(404, 'Customer not found')
    def put(self, customer_id):
        """
        Activate a Customer

        This endpoint will activate a customer
        """
        app.logger.info("Request to activate customer with customer_id: %s", customer_id)
        customer = CustomerModel.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, f"Customer with customer_id '{customer_id}' was not found.")
        customer.is_active = True
        customer.update()
        app.logger.info('Customer with customer_id [%s] has been activated!', customer.customer_id)
        return customer.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /customers/{customer_id}/deactivate
######################################################################
@api.route(f"{BASE_URL}/<int:customer_id>/deactivate", methods=["DELETE"])
@api.param('customer_id', 'The customer identifier')
class DeactivateResource(Resource):
    """ Deactivate actions on a Customer """
    @api.doc('deactivate_customer')
    @api.response(404, 'Customer not found')
    def delete(self, customer_id):
        """
        Deactivate a Customer

        This endpoint will deactivate a customer
        """
        app.logger.info("Request to deactivate customer with customer_id: %s", customer_id)
        customer = CustomerModel.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, f"Customer with customer_id '{customer_id}' was not found.")
        customer.is_active = False
        customer.update()
        app.logger.info('Customer with customer_id [%s] has been deactivated!', customer.customer_id)
        return customer.serialize(), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    CustomerModel.init_db(app)
    AddressModel.init_db(app)
