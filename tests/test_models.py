"""
Test cases for CustomersModel Model

"""
from audioop import add
import os
import logging
import unittest
from datetime import date
from service.models import CustomerModel, AddressModel, Gender, DataValidationError, db
from service import app
from tests.factories import CustomerFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  CUSTOMER   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCustomersModel(unittest.TestCase):
    """ Test Cases for CustomersModel Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        CustomerModel.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(CustomerModel).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_customer(self):
        """It should Create a customer and assert that it exists"""
        customer = CustomerModel(password="password", first_name="Fido", last_name="Lido", nickname="helloFido", email="fido@gmail.com", gender=Gender.MALE, birthday=date(2018, 1, 1))
        self.assertEqual(str(customer), "<CustomerModel 'Fido' customer_id=[None]>")
        self.assertTrue(customer is not None)
        self.assertEqual(customer.customer_id, None)
        self.assertEqual(customer.password, "password")
        self.assertEqual(customer.first_name, "Fido")
        self.assertEqual(customer.last_name, "Lido")
        self.assertEqual(customer.nickname, "helloFido")
        self.assertEqual(customer.email, "fido@gmail.com")
        self.assertEqual(customer.gender, Gender.MALE)
        self.assertEqual(customer.birthday, date(2018, 1, 1))
        
        customer = CustomerModel(password="password", first_name="Fido", last_name="Lido", nickname="helloFido", email="fido@gmail.com", gender=Gender.FEMALE, birthday=date(2018, 1, 1))
        self.assertEqual(customer.gender, Gender.FEMALE)

        customer = CustomerModel(password="password", first_name="Fido", last_name="Lido", nickname="helloFido", email="fido@gmail.com", gender=Gender.UNKNOWN, birthday=date(2018, 1, 1))
        self.assertEqual(customer.gender, Gender.UNKNOWN)
    
    def test_add_a_customer(self):
        """It should Create a customer and add it to the database"""
        customers = CustomerModel.all()
        self.assertEqual(customers, [])
        customer = CustomerModel(password="password", first_name="Fido", last_name="Lido", nickname="helloFido", email="fido@gmail.com", gender=Gender.FEMALE, birthday=date(2018, 1, 1))
        self.assertTrue(customer is not None)
        self.assertEqual(customer.customer_id, None)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(customer.customer_id)
        customers = CustomerModel.all()
        self.assertEqual(len(customers), 1)