#!/usr/bin/python3
""" Places view for handling all default RESTful API actions """
from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route(
    '/cities/<city_id>/places',
    methods=['GET'],
    strict_slashes=False
)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    '/places/<place_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/cities/<city_id>/places',
    methods=['POST'],
    strict_slashes=False
)
def create_place(city_id):
    """Creates a Place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()

    if 'user_id' not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    user = storage.get(User, data['user_id'])
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    data['city_id'] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
