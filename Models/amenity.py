import uuid
from datetime import datetime
from Persistence.data_manager import DataManager


class Amenity(DataManager):
    """class that defines an amenity"""
    amenities = []  # list of existing amenities

    def __init__(self, name: str):
        """initialize an amenity"""
        #if name in Amenity.amenities:
         #   raise ValueError("Amenity already exists")
        Amenity.amenities.append(name)
        self.__id = str(uuid.uuid4())
        self.__created_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")
        self.__updated_at = self.__created_at
        self.__name = name

    @property
    def id(self):
        """id getter"""
        return self.__id

    @property
    def created_at(self):
        """creation datetime getter"""
        return self.__created_at

    @property
    def updated_at(self):
        """last update datetime getter"""
        return self.__updated_at

    @property
    def name(self):
        """name getter"""
        return self.__name

    @name.setter
    def name(self, name):
        """name setter"""
        if type(name) is not str:
            raise TypeError("name must be a text string")
        if not name or len(name.strip()) == 0:
            raise ValueError("name cannot be empty")
        self.__name = name
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

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

        amenity = cls(
            
            name = data['name']
        )
        amenity.__id = data['id']
        amenity.__created_at = data['created_at']
        amenity.__updated_at = data['updated_at']

        return amenity
