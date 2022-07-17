"""
Models for CustomerModel

All of the models are stored in this module
"""
import logging
from enum import Enum
from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import re

from tomlkit import string

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass


class Gender(Enum):
    """Enumeration of valid Customer Genders"""

    MALE = 0
    FEMALE = 1
    UNKNOWN = 3


class CustomerModel(db.Model):
    """
    Class that represents a CustomerModel
    """
    __tablename__ = 'customer'

    app = None

    # Table Schema
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(63), nullable=False)
    first_name = db.Column(db.String(63), nullable=False)
    last_name = db.Column(db.String(63), nullable=False)
    nickname = db.Column(db.String(63), nullable=False)
    email = db.Column(db.String(63), nullable=False)
    gender = db.Column(
        db.Enum(Gender), nullable=False, server_default=(Gender.UNKNOWN.name)
    )
    birthday = db.Column(db.Date(), nullable=False, default=date.today())
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    addresses = db.relationship("AddressModel", cascade="all, delete-orphan")

    def __repr__(self):
        return "<CustomerModel %r customer_id=[%s]>" % (self.first_name, self.customer_id)

    def _email_validator(self, email):
        pattern = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        if not re.match(pattern, email):
            raise DataValidationError(
                "Invalid email address format"
            )
        return email

    def create(self):
        """
        Creates a CustomerModel to the database
        """
        logger.info("Creating %s", self.first_name)
        self.customer_id = None  # customer_id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a CustomerModel to the database
        """
        logger.info("Saving %s", self.first_name)
        db.session.commit()

    def delete(self):
        """ Removes a CustomerModel from the data store """
        logger.info("Deleting %s", self.first_name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a CustomerModel into a dictionary """
        customer = {
            "customer_id": self.customer_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "nickname": self.nickname,
            "email": self._email_validator(self.email),
            "gender": self.gender.name,
            "birthday": self.birthday.isoformat(),
            "password": self.password,
            "addresses": [],
            "is_active": self.is_active
        }
        for address in self.addresses:
            customer["addresses"].append(address.serialize())
        return customer

    def deserialize(self, data):
        """
        Deserializes a CustomerModel from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.first_name = data["first_name"]
            self.last_name = data["last_name"]
            self.nickname = data["nickname"]
            self.email = self._email_validator(data["email"])
            self.password = data["password"]
            # create enum from string
            self.gender = getattr(Gender, data["gender"])
            self.birthday = date.fromisoformat(data["birthday"])
            addresses_list = data.get("addresses")
            for json_address in addresses_list:
                address = AddressModel()
                address.deserialize(json_address)
                self.addresses.append(address)
            self.is_active = data["is_active"]
        except AttributeError as error:
            raise DataValidationError(
                "Invalid attribute: " + error.args[0]
            ) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid CustomerModel: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid CustomerModel: body of request contained bad or no data"
            ) from error
        return self

    @classmethod
    def init_db(cls, app: Flask):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the CustomerModels in the database """
        logger.info("Processing all CustomerModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a CustomerModel by it's customer_id """
        logger.info("Processing lookup for customer_id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, customer_id: int):
        """Find a Customer by it's id

        :param customer_id: the id of the Customer to find
        :type customer_id: int

        :return: an instance with the customer_id, or 404_NOT_FOUND if not found
        :rtype: Customer

        """
        logger.info("Processing lookup or 404 for id %s ...", customer_id)
        return cls.query.get_or_404(customer_id)

    @classmethod
    def find_by_nickname(cls, nickname: string):
        """Find customers by it's nickname"""
        logger.info("Processing lookup for nickname %s ...", nickname)
        return cls.query.filter(CustomerModel.nickname == nickname)
    
    @classmethod
    def find_by_email(cls, email):
        """Returns all Customers with the given Email"""
        logger.info("Processing email query for %s  ...", email)
        return cls.query.filter(cls.email == email)

class AddressModel(db.Model):
    """
    Class that represents a AddressModel
    """
    __tablename__ = 'address'

    app = None

    # Table Schema
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"), nullable=False)
    address_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<AddressModel %r customer_id=[%s] address_id=[%s]>" % (self.address, self.customer_id, self.address_id)

    def create(self):
        """
        Creates a AddressModel to the database
        """
        logger.info("Creating %s", self.address)
        self.address_id = None  # address_id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a AddressModel to the database
        """
        logger.info("Saving %s", self.address_id)
        if not self.address_id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes a AddressModel from the data store """
        logger.info("Deleting %s %s", self.customer_id, self.address_id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a AddressModel into a dictionary """
        return {"customer_id": self.customer_id, "address_id": self.address_id, "address": self.address}

    def deserialize(self, data):
        """
        Deserializes a AddressModel from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.address = data["address"]
            self.address_id = data["address_id"]
            self.customer_id = data["customer_id"]
        except AttributeError as error:
            raise DataValidationError(
                "Invalid attribute: " + error.args[0]
            ) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid AddressModel: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid AddressModel: body of request contained bad or no data"
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the AddressModels in the database """
        logger.info("Processing all AddressModels")
        return cls.query.all()

    @classmethod
    def find_by_customer_id(cls, customer_id):
        logger.info("Processing customer_id query for %s ...", customer_id)
        return cls.query.filter(cls.customer_id == customer_id)


    @classmethod
    def find_by_customer_and_address_id(cls, customer_id, address_id):
        """Get an Address of a Customer
        Args:
            customer_id (int), address_id(int): the customer_id and address_id of the AddressModels you want to match
        """
        logger.info("Processing customer_id and address_id query for %s %s ...", customer_id, address_id)
        return cls.query.filter(cls.customer_id == customer_id).filter(cls.address_id == address_id)

    @classmethod
    def update_address_by_address_and_customer_id(cls, address_id, customer_id, new_address):
        """Update an Address information under address_id

        Args:
            address_id(int): address_id of the AddressModels you want to match
        """
        logger.info("Processing address update for %s ...",  address_id)

        address_found = AddressModel.find_by_customer_and_address_id(address_id, customer_id)
        if address_found.count() == 0:
            raise DataValidationError("the address_id dosen't exist")
        else:
            address_model = address_found[0]
            address_model.address = new_address
            address_model.update()

    @classmethod
    def find_or_404(cls, address_id: int):
        """Find an Address by it's id

        :param address_id: the id of the Customer to find
        :type address_id: int

        :return: an instance with the address_id, or 404_NOT_FOUND if not found
        :rtype: Address

        """
        logger.info("Processing lookup or 404 for id %s ...", address_id)
        return cls.query.get_or_404(address_id)
