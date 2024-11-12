#!/usr/bin/python3
""" Module for the index route of the API.
This module contains the route that return information about the API,
including the status and statistics of objects stored.
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    """Returns the count of each object by type"""
    object_count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(object_count)
