from flask import Blueprint, jsonify, request, abort
from Models.place import Place
from Models.user import User


place_bp = Blueprint("place", __name__)


@place_bp.route("/places", methods=["POST"])
def create_place():
    """Create a new place"""
    data = request.json
    if data is None:
        abort(400, description="No data provided (must be JSON)")
    fields = ["name", "description", "address", "city_id", "latitude",
              "longitude", "rooms", "bathrooms", "price", "max_guests",
              "amenities", "host_id"]
    for field in fields:
        if field not in data:
            abort(400, description=f"Missing {field}")
    user = User.get(data["host_id"], "User")
    if user is None:
        abort(404, description="User not found")
    place = Place(data["name"], data["description"], data["address"],
                  data["city_id"], data["latitude"], data["longitude"],
                  data["rooms"], data["bathrooms"], data["price"],
                  data["max_guests"])
    place.host_id = data["host_id"]
    for amenity in data["amenities"]:
        try:
            place.add_amenity(amenity)
        except ValueError:
            abort(404, description="Amenity not found")
    user.add_place(place.id)
    user.save(user.id, "User", user)
    place.save(place.id, "Place", place)
    user.save(user.id, "User", user)
    return jsonify(place.to_dict()), 201


@place_bp.route("/places", methods=["GET"])
def get_places():
    """Retrieve a list of all places"""
    places = Place.all("Place")
    if places is None:
        abort(404, description="Places not found")
    data = [place for place in places]
    return jsonify(data), 200


@place_bp.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """Retrieve detailed information about a specific place"""
    place = Place.reload(place_id, "Place")
    if place is None:
        abort(404, description="Place not found")
    return jsonify(place), 200


@place_bp.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Update an existing place"""
    place = Place.get(place_id, "Place")
    if place is None:
        abort(404, description="Place not found")
    data = request.json
    if data is None or not data:
        abort(400, description="No data provided (must be JSON)")
    if "host_id" in data:
        user = User.get(data["host_id"], "User")
        if user is None:
            abort(404, description="User not found")
        prev_host = User.get(place.host_id, "User")
        if prev_host is not None and prev_host != user:
            prev_host.places.remove(place_id)
        place.host_id = data["host_id"]
        user.add_place(place_id)
    if "amenities" in data:
        place.amenities.clear()
        place.add_amenity(amenity for amenity in data["amenities"])
    if "name" in data:
        place.name = data["name"]
    if "description" in data:
        place.description = data["description"]
    if "address" in data:
        place.address = data["address"]
    if "city_id" in data:
        place.city_id = data["city_id"]
    if "latitude" in data:
        place.latitude = data["latitude"]
    if "longitude" in data:
        place.longitude = data["longitude"]
    if "rooms" in data:
        place.rooms = data["rooms"]
    if "bathrooms" in data:
        place.bathrooms = data["bathrooms"]
    if "price" in data:
        place.price = data["price"]
    if "max_guests" in data:
        place.max_guests = data["max_guests"]
    place.save(place.id, "Place", place)
    return jsonify(place.to_dict()), 201


@place_bp.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Delete a place"""
    place = Place.get(place_id, "Place")
    if place is None:
        abort(404, description="Place not found")
    host = Place.get(place.host_id, "User")
    # print(host.places)
    # host.places.remove(place_id)
    place.delete(place_id, "Place")
    return "Place deleted", 204
