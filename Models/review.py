import uuid
from datetime import datetime
from Persistence.data_manager import DataManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Review(DataManager):
    """class that defines a review"""
    __tablename__ = 'reviews'

    place_id = db.Column(db.String, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __init__(self, user_id: str, place_id, comment: str, rating: int):
        """initialize a review"""
        self.__id = str(uuid.uuid4())
        self.__created_at = datetime.now().strftime("%B/%d/%Y %I:%M:%S %p")
        self.__updated_at = self.__created_at
        self.__user_id = user_id
        self.__place_id = place_id
        self.__comment = comment
        self.__rating = rating

    def to_dict(self):
        """convert review to dict"""
        return {
            "id": self.__id,
            "created_at": self.__created_at,
            "updated_at": self.__updated_at,
            "user_id": self.__user_id,
            "place_id": self.__place_id,
            "comment": self.__comment,
            "rating": self.__rating,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Review object from a dictionary."""
        review = cls(
            user_id=data['user_id'],
            place_id=data['place_id'],
            comment=data['comment'],
            rating=data['rating']
        )
        review.__id = data['id']
        review.__created_at = data['created_at']
        review.__updated_at = data['updated_at']

        return review
