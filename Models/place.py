import uuid
from datetime import datetime
from .amenity import Amenity
from .review import Review
from Persistence.data_manager import DataManager


class Place(DataManager):
    """class that defines a place"""
    def __init__(self, name: str, description: str, address: str,
                 latitude: float, longitude: float, city_id, rooms: int,
                 bathrooms: int, price: int, max_guests: int):
        """initialize a place"""
        self.__id = str(uuid.uuid4())
        self.__created_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")
        self.__updated_at = self.created_at
        self.__host_id = None
        self.__name = name
        self.__description = description
        self.__address = address
        self.__latitude = latitude
        self.__longitude = longitude
        self.__city_id = city_id
        self.__rooms = rooms
        self.__bathrooms = bathrooms
        self.__price = price
        self.__max_guests = max_guests
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
        #if not isinstance(review, Review):
        #    raise ValueError("review must be a Review instance")
        self.reviews.append(review)
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

    @property
    def id(self):
        """id getter"""
        return self.__id

    @property
    def host_id(self):
        """host id getter"""
        return self.__host_id

    @host_id.setter
    def host_id(self, host_id):
        """host id setter"""
        self.__host_id = host_id
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

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
        if not name or len(name.strip()) == 0:
            raise ValueError("name cannot be empty")
        self.__name = name
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

    @property
    def description(self):
        """description getter"""
        return self.__description

    @description.setter
    def description(self, description):
        """description setter"""
        if not description or len(description.strip()) == 0:
            raise ValueError("description cannot be empty")
        self.__description = description
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

    @property
    def address(self):
        """address getter"""
        return self.__address

    @address.setter
    def address(self, address):
        """address setter"""
        if not address or len(address.strip()) == 0:
            raise ValueError("address cannot be empty")
        self.__address = address
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

    @property
    def latitude(self):
        """latitude getter"""
        return self.__latitude

    @latitude.setter
    def latitude(self, latitude):
        """latitude setter"""
        if type(latitude) is not float:
            raise TypeError("latitude must be a float")
        if not latitude or latitude < -90.0 or latitude > 90.0:
            raise ValueError("latitude must be between -90 and 90")
        self.__latitude = latitude
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

    @property
    def longitude(self):
        """longitude getter"""
        return self.__longitude

    @longitude.setter
    def longitude(self, longitude):
        """longitude setter"""
        if type(longitude) is not float:
            raise TypeError("longitude must be a float")
        if not longitude or longitude < -180.0 or longitude > 180.0:
            raise ValueError("longitude must be between -180 and 180")
        self.__longitude = longitude
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

    @property
    def city_id(self):
        """city getter"""
        return self.__city_id

    @city_id.setter
    def city(self, city_id):
        """city setter"""
        if not city_id or len(city_id.strip()) == 0:
            raise ValueError("city id cannot be empty")
        self.__city_id = city_id
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

    @property
    def rooms(self):
        """rooms getter"""
        return self.__rooms

    @rooms.setter
    def rooms(self, rooms):
        """rooms setter"""
        if type(rooms) is not int:
            raise TypeError("number of rooms must be an integer")
        if not rooms or rooms < 0:
            raise ValueError("number of rooms cannot be a negative number")
        self.__rooms = rooms
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

    @property
    def bathrooms(self):
        """bathrooms getter"""
        return self.__bathrooms

    @bathrooms.setter
    def bathrooms(self, bathrooms):
        """bathrooms setter"""
        if type(bathrooms) is not int:
            raise TypeError("number of bathrooms must be a valid integer")
        if not bathrooms or bathrooms < 0:
            raise ValueError("number of bathrooms cannot be a negative number")
        self.__bathrooms = bathrooms
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

    @property
    def price(self):
        """price getter"""
        return self.__price

    @price.setter
    def price(self, price):
        """price setter"""
        if type(price) is not int:
            raise TypeError("price must be a valid integer")
        if not price or price < 0:
            raise ValueError("price per night cannot be a negative number")
        self.__price = price
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

    @property
    def max_guests(self):
        """maxguests getter"""
        return self.__max_guests

    @max_guests.setter
    def max_guests(self, max_guests):
        """maxguests setter"""
        if type(max_guests) is not int:
            raise TypeError("max guests must be a valid integer")
        if not max_guests or max_guests <= 0:
            raise ValueError("max guests must be atleast 1 guest")
        self.__max_guests = max_guests
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

        place.amenities = [amenity_data for amenity_data in data.get('amenities', [])]

        place.reviews = [review_data for review_data in data.get('reviews', [])]

        return place
