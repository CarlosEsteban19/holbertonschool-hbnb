import uuid
from datetime import datetime
from Persistence.data_manager import DataManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()


class User(DataManager, db.model):
    """class that defines a user"""
    emails = []  # list of existing email addresses
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    places = db.relationship('Place', backref='host', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __init__(self, email: str, first_name: str, last_name: str,
                 password: str, is_admin: bool = False):
        """initialize a user"""
        User.emails.append(email)
        self.email = email
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")
        self.updated_at = self.created_at
        self.first_name = first_name
        self.last_name = last_name
        self.set_password(password)
        self.places = []  # list of places owned by the user
        self.reviews = []  # list of reviews done by the user

    def set_password(self, password):
        """set hashed password"""
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<User {self.id} ({self.email})>"

    def add_place(self, place):
        """Add place to list of user places"""
        self.places.append(place)
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

    def add_review(self, review):
        """Add review to list of user reviews"""
        self.reviews.append(review)
        self.__updated_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")

    def to_dict(self):
        """Convert user to dict"""
        return {
            "id": self.__id,
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "email": self.__email,
            "password": self.__password,
            "created_at": self.__created_at,
            "updated_at": self.__updated_at,
            "places": [place for place in self.places],
            "reviews": [review for review in self.reviews],
        }

    @classmethod
    def from_dict(cls, data):
        """Create a User object from a dictionary."""
        user = cls(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password']
        )
        user.__id = data['id']
        user.__created_at = data['created_at']
        user.__updated_at = data['updated_at']

        user.places = [place_data for place_data in data.get('places', [])]

        user.reviews = [review_data for review_data in data.get('reviews', [])]

        return user
