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

    def test_read_a_customer(self):
        """It should Read a customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.customer_id = None
        customer.create()
        self.assertIsNotNone(customer.customer_id)
        # Fetch it back
        found_customer: CustomerModel = CustomerModel.find(customer.customer_id)
        self.assertEqual(found_customer.customer_id, customer.customer_id)
        self.assertEqual(found_customer.first_name, customer.first_name)
        self.assertEqual(found_customer.last_name, customer.last_name)
        self.assertEqual(found_customer.email, customer.email)
        
######################################################################
#  ADDRESS   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestAddressModel(unittest.TestCase):
    """ Test Cases for AddressModel Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        CustomerModel.init_db(app)
        AddressModel.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(AddressModel).delete()
        db.session.query(CustomerModel).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_create_an_address(self):
        """It should Create an address for a customer and assert that it exists"""
        # create address
        address = AddressModel(customer_id=1, address="address")
        self.assertTrue(address is not None)
        self.assertEqual(str(address), "<AddressModel 'address' customer_id=[1] address_id=[None]>")
        self.assertEqual(address.customer_id, 1)
        self.assertEqual(address.address, "address")
        self.assertEqual(address.address_id, None)
    
    def test_add_an_address(self):
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

        addresses = AddressModel.all()
        self.assertEqual(addresses, [])
        address = AddressModel(customer_id=customer.customer_id, address="address")
        self.assertTrue(address is not None)
        self.assertEqual(str(address), f"<AddressModel 'address' customer_id=[{customer.customer_id}] address_id=[None]>")
        self.assertEqual(address.customer_id, customer.customer_id)
        self.assertEqual(address.address, "address")
        self.assertEqual(address.address_id, None)
        address.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(address.address_id)
        addresses = CustomerModel.all()
        self.assertEqual(len(addresses), 1)

    def test_list_addresses(self):
        """It should list all addresses of a customer"""
        customer_id = 1
        address="address"
        addresses = AddressModel.find_by_customer_id(customer_id)
        self.assertEqual(addresses.count(), 0)

        for i in range(0, 10):
            address_str = f"address{i}"
            address = AddressModel(customer_id=customer_id, address=address_str)
            self.assertTrue(address is not None)
            self.assertEqual(str(address), f"<AddressModel '{address_str}' customer_id=[{customer_id}] address_id=[None]>")
            self.assertEqual(address.customer_id, customer_id)
            self.assertEqual(address.address, address_str)
            self.assertEqual(address.address_id, None)
            address.create()
            # Assert that it was assigned an id and shows up in the database
            self.assertIsNotNone(address.address_id)

        addresses = AddressModel.find_by_customer_id(customer_id)
        self.assertEqual(addresses.count(), 10)

        for i in range(0, 10):
            address_str = f"address{i}"
            address: AddressModel = addresses[i]
            self.assertTrue(address is not None)
            self.assertEqual(address.customer_id, customer_id)
            self.assertEqual(address.address, address_str)
            self.assertIsNotNone(address.address_id)
            
    def test_get_an_address_of_a_customer(self):
        """It should return an address of a customer"""
        customer_id = 1
        address_id = None
        address_prefix="address"

        for i in range(0, 10):
            address_str = f"{address_prefix}{i}"
            address = AddressModel(customer_id=customer_id, address=address_str)
            self.assertTrue(address is not None)
            self.assertEqual(str(address), f"<AddressModel '{address_str}' customer_id=[{customer_id}] address_id=[None]>")
            self.assertEqual(address.customer_id, customer_id)
            self.assertEqual(address.address, address_str)
            self.assertEqual(address.address_id, None)
            address.create()
            # Assert that it was assigned an id and shows up in the database
            self.assertIsNotNone(address.address_id)
            address_id = address.address_id

        found = AddressModel.find_by_customer_and_address_id(customer_id, address_id)
        self.assertEqual(found.count(), 1)
        address = found[0]
        self.assertEqual(address.customer_id, customer_id)
        self.assertEqual(address.address, "address9")
        self.assertEqual(address.address_id, address_id)
        
