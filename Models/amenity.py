import uuid
from datetime import datetime
from Persistence.data_manager import DataManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Amenity(DataManager):
    """class that defines an amenity"""
    amenities = []  # list of existing amenities

    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, name: str):
        """initialize an amenity"""
        Amenity.amenities.append(name)
        self.__id = str(uuid.uuid4())
        self.__created_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")
        self.__updated_at = self.__created_at
        self.__name = name

    def to_dict(self):
        """Return a dictionary representation of an amenity"""
        return {
            "id": self.__id,
            "created_at": self.__created_at,
            "updated_at": self.__updated_at,
            "name": self.__name,
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Amenity object from a dictionary."""

        amenity = cls(name=data['name'])
        amenity.__id = data['id']
        amenity.__created_at = data['created_at']
        amenity.__updated_at = data['updated_at']

        return amenity
