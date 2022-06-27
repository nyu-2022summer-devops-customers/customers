"""
Models for CustomerModel

All of the models are stored in this module
"""
import logging
from enum import Enum
from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import DataError
from sqlalchemy import ForeignKey

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
    __tablename__ = 'customer'

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

    address = db.relationship("AddressModel", backref="customer", lazy=True)

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
        return {
            "customer_id": self.customer_id, 
            "first_name": self.first_name, 
            "last_name": self.last_name, 
            "nickname": self.nickname, 
            "email": self.email, 
            "gender": self.gender.name, 
            "birthday": self.birthday.isoformat(),
            "password": self.password
        }

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
        """Find a Pet by it's id

        :param pet_id: the id of the Pet to find
        :type pet_id: int

        :return: an instance with the pet_id, or 404_NOT_FOUND if not found
        :rtype: Pet

        """
        logger.info("Processing lookup or 404 for id %s ...", customer_id)
        return cls.query.get_or_404(customer_id)

    @classmethod
    def find_by_name(cls, first_name):
        """Returns all CustomerModels with the given first_name

        Args:
            first_name (string): the first_name of the CustomerModels you want to match
        """
        logger.info("Processing first_name query for %s ...", first_name)
        return cls.query.filter(cls.first_name == first_name)
        
class AddressModel(db.Model):
    """
    Class that represents a AddressModel
    """
    __tablename__ = 'address'

    app = None

    # Table Schema
    customer_id = db.Column(db.Integer, ForeignKey("customer.customer_id"),nullable=False)
    address_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(63),nullable=False)

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
        logger.info("Deleting %s %s", self.address_id)
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
    def find(cls, by_id):
        """ Finds a AddressModel by it's address_id """
        logger.info("Processing lookup for address_id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_customer_id(cls, customer_id):
        logger.info("Processing customer_id query for %s ...", customer_id)
        return cls.query.filter(cls.customer_id == customer_id)
    
    
    @classmethod
    def find_by_name(cls, first_name):
        """Returns all AddressModels with the given first_name

        Args:
            first_name (string): the first_name of the AddressModels you want to match
        """
        logger.info("Processing first_name query for %s ...", first_name)
        return cls.query.filter(cls.first_name == first_name)
    
    @classmethod
    def find_by_customer_and_address_id(cls, customer_id, address_id):
        """Get an Address of a Customer
        Args:
            customer_id (int), address_id(int): the customer_id and address_id of the AddressModels you want to match
        """
        logger.info("Processing customer_id and address_id query for %s %s ...", customer_id, address_id)
        return cls.query.filter(cls.customer_id == customer_id).filter(cls.address_id == address_id)
    

    @classmethod
    def find_by_address_id(cls,  address_id):
        """Get an Address information under address_id
        Args:
            address_id(int): address_id of the AddressModels you want to match
        """
        logger.info("Processing address_id query for %s ...",  address_id)
        return cls.query.filter(cls.address_id == address_id)
    
    @classmethod
    def update_address_by_address_id(cls,address_id,new_address):
        """Update an Address information under address_id
        
        Args:
            address_id(int): address_id of the AddressModels you want to match
        """
        logger.info("Processing address update for %s ...",  address_id)
        
        address_found=AddressModel.find_by_address_id(address_id)
        if address_found.count()==0:
            raise DataValidationError("the address_id dosen't exist")
        else:
            address_model=address_found[0]
            address_model.address=new_address
            address_model.update()
        
        


    
    

    

        


