"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
import unittest
from service import app
from service.models import AddressModel, CustomerModel
from service.utils import status
from tests.factories import AddressFactory, CustomerFactory  # HTTP Status Codes

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/customers"


######################################################################
#  T E S T   C U S T O M E R S   S E R V I C E
######################################################################
class TestCustomersService(unittest.TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        self.client = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        pass

    def _create_customers(self, count):
        """Factory method to create customer in bulk"""

        customers = []
        for _ in range(count):
            test_customer = CustomerFactory()
            response = self.client.post(BASE_URL, json=test_customer.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test customer"
            )
            new_customer = response.get_json()
            test_customer.customer_id = new_customer["customer_id"]
            customers.append(test_customer)
        return customers

    def _create_addresses(self, customer_id, count):
        """Factory method to create customer in bulk"""

        addresses = []
        for _ in range(count):
            test_address = AddressFactory()
            test_address.customer_id = customer_id
            response = self.client.post(f"{BASE_URL}/{customer_id}/addresses", json=test_address.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test customer"
            )
            new_customer = response.get_json()
            test_address.address_id = new_customer["address_id"]
            addresses.append(test_address)
        return addresses
    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_customer(self):
        """It should Create a new Customer"""
        test_customer = CustomerFactory()
        logging.debug("Test Customer: %s", test_customer.serialize())
        response = self.client.post(BASE_URL, json=test_customer.serialize())
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)
        logging.debug("Location: %s", location)

        # Check the data is correct
        new_customer = response.get_json()
        self.assertEqual(new_customer["password"], test_customer.password)
        self.assertEqual(new_customer["first_name"], test_customer.first_name)
        self.assertEqual(new_customer["last_name"], test_customer.last_name)
        self.assertEqual(new_customer["nickname"], test_customer.nickname)
        self.assertEqual(new_customer["email"], test_customer.email)
        self.assertEqual(new_customer["gender"], test_customer.gender.name)
        self.assertEqual(new_customer["birthday"], test_customer.birthday.isoformat())

        # Check that the location header was correct
        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_customer = CustomerModel.find(new_customer["customer_id"])
        self.assertNotEqual(new_customer, None)
        new_customer = new_customer.serialize()
        # new_customer = response.get_json()
        self.assertEqual(new_customer["password"], test_customer.password)
        self.assertEqual(new_customer["first_name"], test_customer.first_name)
        self.assertEqual(new_customer["last_name"], test_customer.last_name)
        self.assertEqual(new_customer["nickname"], test_customer.nickname)
        self.assertEqual(new_customer["email"], test_customer.email)
        self.assertEqual(new_customer["gender"], test_customer.gender.name)
        self.assertEqual(new_customer["birthday"], test_customer.birthday.isoformat())

    def test_get_a_customer(self):
        """It should Get a single Customer"""
        # get the id of a pet
        test_customer: CustomerModel = self._create_customers(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_customer.customer_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["customer_id"], test_customer.customer_id)
        self.assertEqual(data["first_name"], test_customer.first_name)
        self.assertEqual(data["last_name"], test_customer.last_name)
        self.assertEqual(data["email"], test_customer.email)

    def test_create_address(self):
        """It should Create a new Customer"""
        test_customer = CustomerFactory()
        logging.debug("Test Customer: %s", test_customer.serialize())
        response = self.client.post(BASE_URL, json=test_customer.serialize())
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)
        logging.debug("Location: %s", location)

        # Check the data is correct
        new_customer = response.get_json()
        self.assertEqual(new_customer["password"], test_customer.password)
        self.assertEqual(new_customer["first_name"], test_customer.first_name)
        self.assertEqual(new_customer["last_name"], test_customer.last_name)
        self.assertEqual(new_customer["nickname"], test_customer.nickname)
        self.assertEqual(new_customer["email"], test_customer.email)
        self.assertEqual(new_customer["gender"], test_customer.gender.name)
        self.assertEqual(new_customer["birthday"], test_customer.birthday.isoformat())

        # Create Address for this customer
        test_address = AddressFactory()
        test_address.customer_id = new_customer["customer_id"]
        logging.debug("Test Address: %s", test_address.serialize())
        response = self.client.post(f"{BASE_URL}/{test_address.customer_id}/addresses", json=test_address.serialize())
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)
        logging.debug("Location: %s", location)

    def test_get_an_address_of_a_customer(self):
        """It should return an address of a customer"""
        customer_id = 1
        addresses = self._create_addresses(customer_id=customer_id, count=10)
        self.assertEqual(len(addresses), 10)
        address_id = addresses[0].address_id
        address_str = addresses[0].address

        response = self.client.get(f"{BASE_URL}/{customer_id}/addresses/{address_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        new_address = response.get_json()
        self.assertEqual(new_address["address_id"], address_id)
        self.assertEqual(new_address["customer_id"], customer_id)
        self.assertEqual(new_address["address"], address_str)
