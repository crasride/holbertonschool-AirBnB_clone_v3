#!/usr/bin/python3
""" The API view for the module status object """
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models.state import State
from models import storage
from models.city import City


# Retrieves the list of all City objects of a State
@app_views.route('/states/<state_id>/cities/',
                 methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """ List of all City objects of a State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    l_cities = state.cities
    d_cities = [city.to_dict()for city in l_cities]
    return jsonify(d_cities)


# Retrieves a City object. : GET /api/v1/cities/<city_id>
@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def city_id_obj(city_id):
    """ City a object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


# Deletes a City object: DELETE /api/v1/cities/<city_id>
@app_views.route('/cities/<city_id>/', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object"""
    n_dict = storage.get(City, city_id)
    if n_dict is None:
        abort(404)
    storage.delete(n_dict)
    storage.save()
    return jsonify({}), 200


# Creates a City: POST /api/v1/states/<state_id>/cities
@app_views.route('/states/<state_id>/cities/',
                 methods=['POST'], strict_slashes=False)
def create_city_with_state_id(state_id):
    """Creates new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    opc_request = request.get_json()
    if opc_request is None:
        return 'Not a JSON', 400
    if 'name' not in opc_request:
        return 'Missing name', 400
    n_city = City(**opc_request)
    n_city.state_id = state_id
    n_city.save()
    return jsonify(n_city.to_dict()), 201


# Updates a City object: PUT /api/v1/cities/<city_id>
@app_views.route('/cities/<city_id>/', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update class City"""
    dict = storage.get(City, city_id)
    if dict is None:
        abort(404)
    opc_request = request.get_json()
    if opc_request is None:
        return 'Not a JSON', 400
    for key in ('id', 'created_at', 'updated_at', 'state_id'):
        opc_request.pop(key, None)
    for key, value in opc_request.items():
        setattr(dict, key, value)
    dict.save()
    return jsonify(dict.to_dict()), 200
