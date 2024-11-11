#!/usr/bin/python3
""" Module for the index route of the API.
This module contains the route that returns the status of the API.
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})
