"""
Models for CustomerModel

All of the models are stored in this module
"""
import logging
from enum import Enum
from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass

class Gender(Enum):
    """Enumeration of valid Pet Genders"""

    MALE = 0
    FEMALE = 1
    UNKNOWN = 3

class CustomerModel(db.Model):
    """
    Class that represents a CustomerModel
    """

    app = None

    # Table Schema
    customer_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(63), nullable=False)
    first_name = db.Column(db.String(63), nullable=False)
    last_name = db.Column(db.String(63), nullable=False)
    nickname = db.Column(db.String(63), nullable=False)
    email = db.Column(db.String(63), nullable=False)
    gender = db.Column(
        db.Enum(Gender), nullable=False, server_default=(Gender.UNKNOWN.name)
    )
    birthday = db.Column(db.Date(), nullable=False, default=date.today())

    def __repr__(self):
        return "<CustomerModel %r customer_id=[%s]>" % (self.first_name, self.customer_id)

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
        return {"customer_id": self.customer_id, "first_name": self.first_name, "last_name": self.last_name, "nickname": self.nickname, "email": self.email, "gender": self.gender.name, "birthday": self.birthday.isoformat(), "password": self.password}

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
            self.email = data["email"]
            self.password = data["password"]
            # create enum from string
            self.gender = getattr(Gender, data["gender"])  
            self.birthday = date.fromisoformat(data["birthday"])
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
        """ Returns all of the CustomerModels in the database """
        logger.info("Processing all CustomerModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a CustomerModel by it's customer_id """
        logger.info("Processing lookup for customer_id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, first_name):
        """Returns all CustomerModels with the given first_name

        Args:
            first_name (string): the first_name of the CustomerModels you want to match
        """
        logger.info("Processing first_name query for %s ...", first_name)
        return cls.query.filter(cls.first_name == first_name)



class AddressesModel(db.Model):
    """
    Class that represents a AddressesModel
    """

    app = None

    # Table Schema
    customer_id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(63))

    def __repr__(self):
        return "<AddressesModel %r customer_id=[%s] address_id=[%s]>" % (self.address, self.customer_id, self.address_id)

    def create(self, customer_id):
        """
        Creates a AddressesModel to the database
        """
        logger.info("Creating %s", self.address)
        self.customer_id = customer_id
        self.address_id = None  # address_id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a AddressesModel to the database
        """
        logger.info("Saving %s", self.first_name)
        db.session.commit()

    def delete(self):
        """ Removes a AddressesModel from the data store """
        logger.info("Deleting %s", self.first_name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a AddressesModel into a dictionary """
        return {"customer_id": self.customer_id, "address_id": self.address_id, "address": self.address}

    def deserialize(self, data):
        """
        Deserializes a AddressesModel from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.address = data["address"]
        except AttributeError as error:
            raise DataValidationError(
                "Invalid attribute: " + error.args[0]
            )
        except KeyError as error:
            raise DataValidationError(
                "Invalid AddressesModel: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid AddressesModel: body of request contained bad or no data"
            )
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
        """ Returns all of the AddressesModels in the database """
        logger.info("Processing all AddressesModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a AddressesModel by it's customer_id """
        logger.info("Processing lookup for customer_id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, first_name):
        """Returns all AddressesModels with the given first_name

        Args:
            first_name (string): the first_name of the AddressesModels you want to match
        """
        logger.info("Processing first_name query for %s ...", first_name)
        return cls.query.filter(cls.first_name == first_name)
