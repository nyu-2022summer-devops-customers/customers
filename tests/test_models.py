"""
Test cases for CustomersModel Model
"""
# from audioop import add
from werkzeug.exceptions import NotFound
import os
import logging
import unittest
from datetime import date
from service.models import CustomerModel, AddressModel, Gender, DataValidationError, db
from service import app
from tests.factories import CustomerFactory
from tests.factories import AddressFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
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
        db.session.query(AddressModel).delete()
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
        customer = CustomerModel(password="password", first_name="Fido", last_name="Lido", nickname="helloFido",
                                 email="fido@gmail.com", gender=Gender.MALE, birthday=date(2018, 1, 1), is_active=True)
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
        self.assertEqual(customer.is_active, True)

        customer = CustomerModel(password="password", first_name="Fido", last_name="Lido", nickname="helloFido",
                                 email="fido@gmail.com", gender=Gender.FEMALE, birthday=date(2018, 1, 1), is_active=True)
        self.assertEqual(customer.gender, Gender.FEMALE)

        customer = CustomerModel(password="password", first_name="Fido", last_name="Lido", nickname="helloFido",
                                 email="fido@gmail.com", gender=Gender.UNKNOWN, birthday=date(2018, 1, 1,), is_active=True)
        self.assertEqual(customer.gender, Gender.UNKNOWN)

    def test_add_a_customer(self):
        """It should Create a customer and add it to the database"""
        customers = CustomerModel.all()
        self.assertEqual(customers, [])
        customer = CustomerModel(password="password", first_name="Fido", last_name="Lido", nickname="helloFido",
                                 email="fido@gmail.com", gender=Gender.FEMALE, birthday=date(2018, 1, 1), is_active=True)
        self.assertTrue(customer is not None)
        self.assertEqual(customer.customer_id, None)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(customer.customer_id)
        customers = CustomerModel.all()
        self.assertEqual(len(customers), 1)

    def test_update_a_customer(self):
        """It should Update a Customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.customer_id = None
        customer.create()
        logging.debug(customer)
        self.assertIsNotNone(customer.customer_id)
        # Change it an save it
        customer.gender = Gender.MALE
        original_id = customer.customer_id
        customer.update()
        self.assertEqual(customer.customer_id, original_id)
        self.assertEqual(customer.gender, Gender.MALE)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = CustomerModel.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].customer_id, original_id)
        self.assertEqual(customers[0].gender, Gender.MALE)

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
        self.assertEqual(found_customer.is_active, customer.is_active)
        self.assertEqual(found_customer.is_active, True)

    def test_list_all_customers(self):
        """It should List all Customers in the database"""
        customers = CustomerModel.all()
        self.assertEqual(customers, [])
        # Create 5 Customers
        for i in range(5):
            customer = CustomerFactory()
            customer.create()
        # See if we get back 5 customers
        customers = CustomerModel.all()
        self.assertEqual(len(customers), 5)

    def test_delete_a_customer(self):
        """It should Delete a Customer"""
        customers = CustomerModel.all()
        self.assertEqual(customers, [])
        customer = CustomerModel(password="password", first_name="Fido", last_name="Lido", nickname="helloFido",
                                 email="fido@gmail.com", gender=Gender.FEMALE, birthday=date(2018, 1, 1), is_active=True)
        self.assertTrue(customer is not None)
        self.assertEqual(customer.customer_id, None)
        customer.create()
        customers = CustomerModel.all()
        self.assertEqual(len(customers), 1)
        # delete the customer and make sure it isn't in the database
        customer.delete()
        customers = CustomerModel.all()
        self.assertEqual(len(customers), 0)

    def test_delete_a_customer_with_addresses(self):
        """It should Delete a Customer and All Addresses Related to This Customer"""
        # create a customer
        customers = CustomerModel.all()
        self.assertEqual(customers, [])
        customer = CustomerModel(
            password="password",
            first_name="Fido",
            last_name="Lido",
            nickname="helloFido",
            email="fido@gmail.com",
            gender=Gender.FEMALE,
            birthday=date(2018, 1, 1)
        )
        self.assertTrue(customer is not None)
        self.assertEqual(customer.customer_id, None)

        # create addresses for this customer
        address = AddressFactory()
        customer.addresses.append(address)
        customer.create()

        customers = CustomerModel.all()
        self.assertEqual(len(customers), 1)
        self.assertNotEqual(customer.customer_id, None)
        addresses = AddressModel.find_by_customer_id(customer_id=customer.customer_id)
        self.assertEqual(addresses.count(), 1)

        # delete the customer and make sure all addresses related to the record are not in the database
        customer.delete()
        customers = CustomerModel.all()
        addresses = AddressModel.find_by_customer_id(customer_id=customer.customer_id)
        self.assertEqual(len(customers), 0)
        self.assertEqual(addresses.count(), 0)

    def test_serialize_a_customer(self):
        """It should serialize a Customer"""
        customer = CustomerFactory()
        data = customer.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("customer_id", data)
        self.assertEqual(data["customer_id"], customer.customer_id)
        self.assertIn("first_name", data)
        self.assertEqual(data["first_name"], customer.first_name)
        self.assertIn("last_name", data)
        self.assertEqual(data["last_name"], customer.last_name)
        self.assertIn("nickname", data)
        self.assertEqual(data["nickname"], customer.nickname)
        self.assertIn("email", data)
        self.assertEqual(data["email"], customer.email)
        self.assertIn("gender", data)
        self.assertEqual(data["gender"], customer.gender.name)
        self.assertIn("password", data)
        self.assertEqual(data["password"], customer.password)
        self.assertIn("birthday", data)
        self.assertEqual(date.fromisoformat(data["birthday"]), customer.birthday)
        self.assertIn("is_active", data)
        self.assertEqual(data["is_active"], customer.is_active)

    def test_deserialize_a_customer(self):
        """It should de-serialize a Customer"""
        test_customer = CustomerFactory()
        test_address = AddressFactory()
        test_customer.addresses.append(test_address)
        data = test_customer.serialize()
        customer = CustomerModel()
        customer.deserialize(data)
        self.assertNotEqual(customer, None)
        self.assertEqual(customer.customer_id, data["customer_id"])
        self.assertEqual(customer.first_name, data["first_name"])
        self.assertEqual(customer.last_name, data["last_name"])
        self.assertEqual(customer.nickname, data["nickname"])
        self.assertEqual(customer.email, data["email"])
        self.assertEqual(customer.gender.name, data["gender"])
        self.assertEqual(customer.password, data["password"])
        self.assertEqual(customer.birthday, date.fromisoformat(data["birthday"]))
        self.assertEqual(customer.is_active, data["is_active"])

    def test_deserialize_a_customer_without_customer_id(self):
        """It should de-serialize a Customer without customer_id"""
        test_customer = CustomerFactory()
        test_address = AddressFactory()
        test_customer.addresses.append(test_address)
        data = test_customer.serialize()
        data.pop("customer_id")
        customer = CustomerModel()
        customer.deserialize(data)
        self.assertNotEqual(customer, None)
        self.assertEqual(customer.customer_id, None)
        self.assertEqual(customer.first_name, data["first_name"])
        self.assertEqual(customer.last_name, data["last_name"])
        self.assertEqual(customer.nickname, data["nickname"])
        self.assertEqual(customer.email, data["email"])
        self.assertEqual(customer.gender.name, data["gender"])
        self.assertEqual(customer.password, data["password"])
        self.assertEqual(customer.birthday, date.fromisoformat(data["birthday"]))
        self.assertEqual(customer.is_active, data["is_active"])

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        test_customer = CustomerModel()
        self.assertRaises(DataValidationError, test_customer.deserialize, data)

    def test_deserialize_a_customer_with_type_error(self):
        """ Deserialize a Customer with a TypeError """
        test_customer = CustomerModel()
        self.assertRaises(DataValidationError, test_customer.deserialize, [])

    def test_deserialize_a_customer_with_key_error(self):
        """ Deserialize a Customer with a KeyError """
        test_customer = CustomerModel()
        self.assertRaises(DataValidationError, test_customer.deserialize, {})

    def test_deserialize_missing_data(self):
        """It should not deserialize a Customer with missing data"""
        data = {"customer_id": 1, "first_name": "Kitty", "last_name": "cat"}
        test_customer = CustomerModel()
        self.assertRaises(DataValidationError, test_customer.deserialize, data)

    def test_deserialize_bad_email(self):
        """It should not deserialize a Customer with missing data"""
        test_customer = CustomerFactory()
        data = test_customer.serialize()
        data["email"] = "this is not an email"
        self.assertRaises(DataValidationError, test_customer.deserialize, data)

    def test_deserialize_bad_gender(self):
        """ Deserialize a Customer with a bad gender attribute """
        test_customer = CustomerFactory()
        data = test_customer.serialize()
        data["gender"] = "male"
        customer = CustomerModel()
        self.assertRaises(DataValidationError, customer.deserialize, {})

    def test_find_by_email(self):
        """It should return a customer list found by email"""
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()
        customer_list = CustomerModel.find_by_email(email=customers[0].email)
        self.assertIsNot(customer_list.count(), 0)
        for customer in customer_list:
            self.assertEqual(customer.email, customers[0].email)

    def test_find_by_non_existing_email(self):
        """It should return an empty customer list found by non-existing email"""
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()
        customer_list = CustomerModel.find_by_email("not-exist@nyu.edu")
        self.assertEqual(customer_list.count(), 0)

    def test_find_customer_by_nickname(self):
        """It should return a customer list found by nickname"""
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()
        customer_list = CustomerModel.find_by_nickname(nickname=customers[0].nickname)
        self.assertIsNot(customer_list.count(), 0)
        for customer in customer_list:
            self.assertEqual(customer.nickname, customers[0].nickname)

    def test_find_customer_by_non_existing_nickname(self):
        """It should return an empty customer list found by nickname"""
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()
        customer_list = CustomerModel.find_by_nickname("not-exist")
        self.assertEqual(customer_list.count(), 0)

    # def test_find_customer_by_name(self):
    #     """It should return a customer list found by name"""
    #     customers = CustomerFactory.create_batch(3)
    #     for customer in customers:
    #         customer.create()
    #     firstname = customers[0].first_name
    #     lastname = customers[0].last_name
    #     customer_list = CustomerModel.find_by_name(firstname, lastname)
    #     self.assertIsNot(customer_list.count(), 0)
    #     for customer in customer_list:
    #         self.assertEqual(customer.first_name, customers[0].first_name)
    #         self.assertEqual(customer.last_name, customers[0].last_name)

    def test_find_customer_by_non_existing_name(self):
        """It should return an empty customer list found by name"""
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()
        customer_list = CustomerModel.find_by_name("firstname", "lastname")
        self.assertEqual(customer_list.count(), 0)

    def test_find_customer_by_birthday(self):
        """It should return a customer list found by birthday"""
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()
        birthday = customers[0].birthday
        customer_list = CustomerModel.find_by_birthday(birthday)
        self.assertIsNot(customer_list.count(), 0)
        for customer in customer_list:
            self.assertEqual(customer.birthday, customers[0].birthday)

    def test_find_customer_by_non_existing_birthday(self):
        """It should return an empty customer list found by birthday"""
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()
        customer_list = CustomerModel.find_by_birthday("9999-09-09")
        self.assertEqual(customer_list.count(), 0)

    def test_find_or_404_not_found(self):
        """ Find or return 404 NOT found """
        self.assertRaises(NotFound, CustomerModel.find_or_404, 0)
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
        customer = CustomerModel(password="password", first_name="Fido", last_name="Lido", nickname="helloFido",
                                 email="fido@gmail.com", gender=Gender.FEMALE, birthday=date(2018, 1, 1), is_active=True)
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

    def test_delete_address(self):
        """ Delete an Address """
        customer = CustomerFactory()
        customer.create()
        id = customer.customer_id
        address = AddressFactory()
        address.customer_id = id
        address.create()
        self.assertEqual(len(AddressModel.all()), 1)
        # delete the address and make sure it isn't in the database
        address.delete()
        customer.delete()
        self.assertEqual(len(AddressModel.all()), 0)

    def test_list_addresses(self):
        """It should list all addresses of a customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.customer_id = None
        customer.create()

        customer_id = customer.customer_id
        address = "address"
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
        customer = CustomerFactory()
        logging.debug(customer)
        customer.customer_id = None
        customer.create()

        customer_id = customer.customer_id
        address_id = None
        address_prefix = "address"

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

    def test_update_an_address(self):
        """It should Update a AddressModel"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.customer_id = None
        customer.create()
        customer_id = customer.customer_id
        address = AddressFactory()
        logging.debug(address)
        address.address_id = None
        address.customer_id = customer_id
        address.create()
        logging.debug(address)
        self.assertIsNotNone(address.address_id)
        # Change it an save it
        address.address = "new_address"
        original_id = address.address_id
        address.update()
        self.assertEqual(address.address_id, original_id)
        self.assertEqual(address.address, "new_address")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        addresses = AddressModel.all()
        self.assertEqual(len(addresses), 1)
        self.assertEqual(addresses[0].address_id, original_id)
        self.assertEqual(addresses[0].address, "new_address")

    def test_update_an_address_by_customer_and_address_id(self):
        """It should Update a AddressModel by address id"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.customer_id = None
        customer.create()
        customer_id = customer.customer_id
        address = AddressFactory()
        logging.debug(address)
        address.address_id = None
        address.customer_id = customer_id
        address.create()
        logging.debug(address)
        self.assertIsNotNone(address.address_id)
        # Change it an save it
        AddressModel.update_address_by_address_and_customer_id(address.customer_id, address.address_id, "new_address")
        original_id = address.address_id
        self.assertEqual(address.address_id, original_id)
        self.assertEqual(address.address, "new_address")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        addresses = AddressModel.all()
        self.assertEqual(len(addresses), 1)
        self.assertEqual(addresses[0].address_id, original_id)
        self.assertEqual(addresses[0].address, "new_address")

    def test_update_by_customer_and_address_no_address_id(self):
        """It should not Update a Address without an address_id"""
        address = AddressFactory()
        logging.debug(address)
        address.address_id = None
        self.assertRaises(DataValidationError, address.update)
        address = AddressFactory()
        logging.debug(address)
        address.address_id = None
        with self.assertRaises(DataValidationError):
            AddressModel.update_address_by_address_and_customer_id(address.customer_id, address.address_id, "new_address")

    def test_update_no_address_id(self):
        """It should not Update a Address by id without an address_id"""
        address = AddressFactory()
        logging.debug(address)
        address.address_id = None
        self.assertRaises(DataValidationError, address.update)

    def test_serialize_an_address(self):
        """It should serialize a Address"""
        address = AddressFactory()
        data = address.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("customer_id", data)
        self.assertEqual(data["customer_id"], address.customer_id)
        self.assertIn("address_id", data)
        self.assertEqual(data["address_id"], address.address_id)
        self.assertIn("address", data)
        self.assertEqual(data["address"], address.address)

    def test_deserialize_an_address(self):
        """It should de-serialize an Address"""
        data = AddressFactory().serialize()
        address = AddressModel()
        address.deserialize(data)
        self.assertNotEqual(address, None)
        self.assertEqual(address.address_id, data["address_id"])
        self.assertEqual(address.customer_id, data["customer_id"])
        self.assertEqual(address.address, data["address"])

    def test_deserialize_an_address_without_address_id(self):
        """It should de-serialize an Address without address id"""
        data = AddressFactory().serialize()
        data.pop("address_id")
        address = AddressModel()
        address.deserialize(data)
        self.assertNotEqual(address, None)
        self.assertEqual(address.address_id, None)
        self.assertEqual(address.customer_id, data["customer_id"])
        self.assertEqual(address.address, data["address"])

    def test_deserialize_an_address_with_type_error(self):
        """ Deserialize an Address with a TypeError """
        address = AddressModel()
        self.assertRaises(DataValidationError, address.deserialize, [])

    def test_deserialize_an_address_with_key_error(self):
        """ Deserialize an Address with a KeyError """
        address = AddressModel()
        self.assertRaises(DataValidationError, address.deserialize, {})

    def test_delete_an_address_of_a_customer(self):
        """It should delete an address of a customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.customer_id = None
        customer.create()

        customer_id = customer.customer_id
        address_id = None
        address_prefix = "address"

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
        found.delete()
        self.assertEqual(found.count(), 0)

    def test_find_or_404_found_address(self):
        """It should Find an address or return 404 not found"""
        test_customer = CustomerFactory()
        test_customer.create()
        addresses = AddressFactory.create_batch(3)
        for address in addresses:
            address.customer_id = test_customer.customer_id
            address.create()

        address = AddressModel.find_or_404(addresses[1].address_id)
        self.assertIsNot(address, None)
        self.assertEqual(address.customer_id, addresses[1].customer_id)
        self.assertEqual(address.address, addresses[1].address)
        self.assertEqual(address.address_id, addresses[1].address_id)

    def test_find_or_404_not_found_address(self):
        """It should return 404 not found for an Address"""
        self.assertRaises(NotFound, AddressModel.find_or_404, 0)
