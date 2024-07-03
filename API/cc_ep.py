from flask import Blueprint, jsonify, request, abort
from Models.country import Country
from Models.city import City


cc_bp = Blueprint("cc", __name__)


@cc_bp.route("/countries", methods=["GET"])
def get_countries():
    """Retrieve all pre-loaded countries"""
    countries = Country.all()
    return jsonify(countries), 200


@cc_bp.route("/countries/<country_code>", methods=["GET"])
def get_country(country_code):
    """Retrieve details of a specific country by its code"""
    country = Country.get(country_code)
    if country is None:
        abort(404, description="Country not found")
    return jsonify(country), 200


@cc_bp.route("/countries/<country_code>/cities", methods=["GET"])
def get_cities_in_country(country_code):
    """Retrieve all cities belonging to a specific country"""
    country = Country.get(country_code)
    if not country:
        abort(404, description="Country not found")
    cities = [city for city in City.all("City")
              if city["country_code"] == country_code]
    if not cities:
        abort(404, description="Cities not found")
    return jsonify(cities), 200


@cc_bp.route("/cities", methods=["POST"])
def create_city():
    """Create a new city"""
    data = request.json
    if data is None:
        abort(400, description="No data provided (must be JSON)")
    fields = ["name", "country_code"]
    for field in fields:
        if field not in data:
            abort(400, description=f"Missing {field}")
    city = City(data["name"], data["country_code"])
    city.save(city.id, "City", city)
    return jsonify(city.to_dict()), 200


@cc_bp.route("/cities", methods=["GET"])
def get_cities():
    """Retrieve all cities"""
    cities = City.all("City")
    if cities is None:
        abort(404, description="No cities found")
    cities_data = [city for city in cities]
    if cities_data is None:
        abort(404, description="No cities found")
    return jsonify(cities_data), 200


@cc_bp.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """Retrieve details of a specific city"""
    city = City.reload(city_id, "City")
    if city is None:
        abort(404, description="City not found")
    return jsonify(city), 200


@cc_bp.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """Update an existing city"""
    city = City.get(city_id, "City")
    if city is None:
        abort(400, description="City not found")
    data = request.json
    if data is None:
        abort(400, description="No data provided (must be JSON)")
    if "name" in data:
        city.name = data["name"]
    if "country_code" in data:
        city.country_code = data["country_code"]
    city.update(city.id, "City", city)
    return jsonify(city.to_dict()), 201


@cc_bp.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Celete a city"""
    city = City.get(city_id, "City")
    if city is None:
        abort(400, description="City not found")
    city.delete(city.id, "City")
    return "City deleted", 204
