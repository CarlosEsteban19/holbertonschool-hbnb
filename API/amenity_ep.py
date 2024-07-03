from flask import Blueprint, jsonify, request, abort
from Models.amenity import Amenity

amenity_bp = Blueprint("amenity", __name__)


@amenity_bp.route("/amenities", methods=["POST"])
def create_ammenity():
    """Create a new ammenity"""
    data = request.json
    if data is None:
        abort(400, description="No data provided (must be JSON)")
    if "name" not in data:
        abort(400, description="Missing name")
    if data["name"] in Amenity.amenities:
        abort(400, description="Amenity already exists")
    amenity = Amenity(data["name"])
    amenity.save(amenity.id, "Amenity", amenity)
    return jsonify(amenity.to_dict()), 201


@amenity_bp.route("/amenities", methods=["GET"])
def get_ammenities():
    """Retrieve a list of all amenities"""
    amenities = Amenity.all("Amenity")
    if amenities is None:
        abort(404, description="No amenities found")
    data = [amenity for amenity in amenities]
    return jsonify(data), 200


@amenity_bp.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """Retrieve detailed information about a specific amenity"""
    amenity = Amenity.reload(amenity_id, "Amenity")
    if amenity is None:
        abort(404, description="Amenity not found")
    return jsonify(amenity), 200


@amenity_bp.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """Update an existing amenity"""
    amenity = Amenity.get(amenity_id, "Amenity")
    if amenity is None:
        abort(404, description="Amenity not found")
    data = request.json
    if data is None:
        abort(400, description="No data provided (must be JSON)")
    if "name" in data:
        amenity.name = data["name"]
    amenity.update(amenity.id, "Amenity", amenity)
    return jsonify(amenity.to_dict()), 201


@amenity_bp.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Delete an amenity"""
    amenity = Amenity.get(amenity_id, "Amenity")
    if amenity is None:
        abort(404, description="Amenity not found")
    amenity.delete(amenity.id, "Amenity")
    return "Amenity deleted", 204
