import uuid
from datetime import datetime
from Persistence.data_manager import DataManager
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class City(DataManager):
    """class that defines a city"""
    __tablename__ = 'cities'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    country_code = db.Column(
        db.String(3), db.ForeignKey('countries.code'), nullable=False)
    country = db.relationship('Country', back_populates='cities')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, name: str, country_code):
        """initialize a city"""
        self.__id = str(uuid.uuid4())
        self.__created_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")
        self.__updated_at = self.__created_at
        self.__name = name
        self.__country_code = country_code

    def to_dict(self):
        """Return a dictionary representation of a city"""
        return {
            "id": self.__id,
            "created_at": self.__created_at,
            "updated_at": self.__updated_at,
            "name": self.__name,
            "country_code": self.__country_code
        }

    @classmethod
    def from_dict(cls, data):
        """Create a City object from a dictionary."""
        city = cls(
            name=data['name'],
            country_code=data['country_code']
        )
        city.__id = data['id']
        city.__created_at = data['created_at']
        city.__updated_at = data['updated_at']

        return city
