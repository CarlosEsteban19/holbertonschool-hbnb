import uuid
from datetime import datetime
from .amenity import Amenity
from Persistence.data_manager import DataManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Place(DataManager):
    """class that defines a place"""
    __tablename__ = 'places'

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    host_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    city_id = db.Column(db.String, db.ForeignKey('cities.id'), nullable=False)
    price_per_night = db.Column(db.Integer, nullable=False)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    number_of_bathrooms = db.Column(db.Integer, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)

    host = db.relationship('User', back_populates='places')
    city = db.relationship('City', back_populates='places')

    def __init__(self, name: str, description: str, address: str,
                 latitude: float, longitude: float, city_id, rooms: int,
                 bathrooms: int, price: int, max_guests: int):
        """initialize a place"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")
        self.updated_at = self.created_at
        self.host_id = None
        self.name = name
        self.description = description
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.city_id = city_id
        self.rooms = rooms
        self.bathrooms = bathrooms
        self.price = price
        self.max_guests = max_guests
        self.amenities = []  # list of amenities belonging to this place
        self.reviews = []  # list of reviews belonging to this place

    def add_amenity(self, amenity):
        """adds amenity to place amenities"""
        if amenity not in Amenity.amenities:
            raise ValueError("Amenity does not exist")
        self.amenities.append(amenity)
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

    def add_review(self, review):
        """adds review to place reviews"""
        self.reviews.append(review)
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

    def to_dict(self):
        """convert place to dict"""
        return {
            "id": self.__id,
            "host_id": self.__host_id,
            "created_at": self.__created_at,
            "updated_at": self.__updated_at,
            "name": self.__name,
            "description": self.__description,
            "address": self.__address,
            "latitude": self.__latitude,
            "longitude": self.__longitude,
            "city_id": self.__city_id,
            "rooms": self.__rooms,
            "bathrooms": self.__bathrooms,
            "price": self.__price,
            "max_guests": self.__max_guests,
            "amenities": [amenity for amenity in self.amenities],
            "reviews": [review for review in self.reviews],
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Place object from a dictionary."""
        place = cls(
            name=data['name'],
            description=data['description'],
            address=data['address'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            city_id=data['city_id'],
            rooms=int(data['rooms']),
            bathrooms=int(data['bathrooms']),
            price=int(data['price']),
            max_guests=int(data['max_guests'])
        )
        place.__id = data['id']
        place.__created_at = data['created_at']
        place.__updated_at = data['updated_at']
        place.__host_id = data['host_id']

        place.amenities = [
            amenity_data for amenity_data in data.get('amenities', [])]

        place.reviews = [
            review_data for review_data in data.get('reviews', [])]

        return place
